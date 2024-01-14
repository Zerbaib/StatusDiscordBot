from utils.var import *
from utils.sql import create_database
from utils.updateServerCount import update_server_count
from disnake import Intents
from disnake.ext import commands
from asyncio import sleep
from json import load, dump
from os import path

if not path.exists(database_path):
    create_database(database_path)

if not path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        dump(config_data, config_file, indent=4)
else:
    with open(config_file_path, 'r') as config_file:
        config = load(config_file)

token = config["TOKEN"]
chan = config["CHAN_ID"]
you = config["YOUR_ID"]
sec_loop = config["sec_loop"]
del_time = config["del_time"]

bot = commands.Bot(command_prefix='!', intents=Intents.all())

@bot.event
async def on_ready():
    print("done")
    await update_server_count(bot, sec_loop)
    print(f'Logged in as {bot.user.name}')


async def update_servers_status():
    await bot.wait_until_ready()
    user = await bot.fetch_user(you)
    server_channel = bot.get_channel(chan)
    embed_message = None
    msg_id = config["MSG_ID"]

    if msg_id:
        try:
            embed_message = await server_channel.fetch_message(msg_id)
        except disnake.NotFound:
            errors.tree01()
            pass

    while not bot.is_closed():
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)

        embed = disnake.Embed(
            title='Status of servers',
            colour=disnake.Color.old_blurple())
        for server in servers:
            stats = ''
            name = server['name']
            ip = server['ip']
            maintenance = server.get('maintenance')
            not_installed = server.get('not_installed')

            if maintenance:
                status = statues.idle
                ping_result = 'N/A'
            elif not_installed:
                status = statues.not_h
                ping_result = 'N/A'
            else:
                status, ping_result = await ping_server(ip)
                if status == "Online":
                    stats = "Online"
                    status = statues.on
                else:
                    stats = "Offline"
                    status = statues.off
                
            if stats == 'Offline' and server['alert'] == False:
                alert_s = alerts.shutdown(name)
                await user.send(embed=alert_s)
                server['alert'] = True
            if stats == 'Online' and server['alert'] == True:
                alert_b = alerts.boot(name)
                await user.send(embed=alert_b)
                server['alert'] = False

            embed.add_field(
                name=name,
                value=f'{status} With ``{ping_result}``',
                inline=False
                )

        embed.add_field(
            name="legend",
            value=f"If is {statues.on} the server is online!\n"
                  f"If is {statues.idle} the server has bugs.\n"
                  f"If is {statues.off} the server is offline.\n"
                  f"If is {statues.not_h} the server is not installed.",
            inline=False
        )

        if embed_message:
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)
            msg_id = embed_message.id
            errors.tree02()

            # Sauvegarder l'ID du message dans le fichier de configuration
            config["MSG_ID"] = msg_id
            with open(config_file_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            errors.tree03()

        save_servers(servers)  # Save server configuration

        await asyncio.sleep(sec_loop)
