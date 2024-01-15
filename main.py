from utils.var import *
from utils.sql import create_database
from utils.alerts import *
from utils.updateServerCount import update_server_count
from disnake import Intents, NotFound, Embed
from disnake.ext import commands
from asyncio import sleep
import aioping
from json import load, dump
from os import path

if not path.exists(database_path):
    create_database(database_path)

if not path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        dump(config_data, config_file, indent=4)

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
        except NotFound:
            pass

    while not bot.is_closed():
        with open('servers.json', 'r') as servers_file:
            servers = load(servers_file)

        embed = Embed(
            title='Status of servers',
            colour=blurple)
        for server in servers:
            stats = ''
            name = server['name']
            ip = server['ip']
            maintenance = server.get('maintenance')
            not_installed = server.get('not_installed')

            if maintenance:
                status = idle
                ping_result = 'N/A'
            elif not_installed:
                status = not_h
                ping_result = 'N/A'
            else:
                status, ping_result = await ping_server(ip)
                if status == "Online":
                    stats = "Online"
                    status = on
                else:
                    stats = "Offline"
                    status = off
                
            if stats == 'Offline' and server['alert'] == False:
                alert_s = down(name)
                await user.send(embed=alert_s)
                server['alert'] = True
            if stats == 'Online' and server['alert'] == True:
                alert_b = up(name)
                await user.send(embed=alert_b)
                server['alert'] = False

            embed.add_field(
                name=name,
                value=f'{status} With ``{ping_result}``',
                inline=False
                )

        embed.add_field(
            name="legend",
            value=f"If is {on} the server is online!\n"
                  f"If is {idle} the server has bugs.\n"
                  f"If is {off} the server has problem.\n"
                  f"If is {not_h} the server is offline.",
            inline=False
        )

        if embed_message:
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)
            msg_id = embed_message.id

            # Sauvegarder l'ID du message dans le fichier de configuration
            config["MSG_ID"] = msg_id
            with open(config_file_path, 'w') as config_file:
                dump(config, config_file, indent=4)

        await sleep(sec_loop)
