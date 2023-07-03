import disnake
from disnake.ext import commands
from utils import alerts, statues, msg, errors
import asyncio
import subprocess
import json
import os

servers_file_path = 'servers.json'
config_file_path = 'config.json'
config_data = {
    "TOKEN": "your_bot_token",
    "CHAN_ID": 1234567890,
    "MSG_ID": None,
    "YOUR_ID": 1234567890,
    "sec_loop": 60,
    "del_time": 3
}

if not os.path.exists(servers_file_path):
    with open(servers_file_path, 'w') as servers_file:
        servers_file.write('[]')

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    errors.one01()
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    if config_data == config:
        errors.one02()

token = config["TOKEN"]
chan = config["CHAN_ID"]
you = config["YOUR_ID"]
sec_loop = config["sec_loop"]
del_time = config["del_time"]

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

@bot.event
async def on_ready():
    await update_server_count()  # Met à jour le nombre de serveurs au démarrage
    print(f'Logged in as {bot.user.name}')

def save_servers(servers):
    with open('servers.json', 'w') as servers_file:
        json.dump(servers, servers_file, indent=4, ensure_ascii=False)

async def update_server_count():
    while not bot.is_closed():
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)

        servers_count = len(servers)
        activity = disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f'{servers_count} servers'
        )
        await bot.change_presence(activity=activity)

        await asyncio.sleep(sec_loop)  # Attendre un certain intervalle avant la prochaine mise à jour

async def ping_server(ip):
    if ip == 'not here':
        return 'Not Here', 'N/A'

    try:
        result = await asyncio.create_subprocess_shell(
            f'ping -c 1 {ip}', stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, _ = await result.communicate()
        output = output.decode('utf-8')
        if result.returncode == 0:
            start_index = output.find('time=')
            if start_index != -1:
                end_index = output.find(' ms', start_index)
                if end_index != -1:
                    ping_time = output[start_index + 5:end_index]
                    return 'Online', f'{ping_time} ms'
            return 'Online', 'N/A'
        else:
            return 'Offline', 'N/A'
    except Exception:
        errors.two01()
        return 'Erreur lors du ping', 'N/A'

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

bot.loop.create_task(update_servers_status())
bot.loop.create_task(update_server_count())

@bot.slash_command(
    name="maintenance",
    description="Enable or disable maintenance mode for a server"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, server: str, option: str):
    if ctx.author.id != you:
        await ctx.send("You are not authorized to execute this command.")
        return

    valid_options = ['idle', 'not_here']
    if option.lower() not in valid_options:
        embed = disnake.Embed(title="Invalid option !", 
                              description=f"Only 2 option is possible:\n\n"
                                          f"**For orange mode:**```idle```\n"
                                          f"**For grey mode:**```not_here```",
                              color=disnake.Color.red())
        await ctx.send(embed=embed, delete_after=del_time)
        return

    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    server = next((s for s in servers if s['name'].lower() == server.lower()), None)

    if server:
        if option.lower() == 'idle':
            if server['maintenance'] == False:
                server['maintenance'] = True
                status = "True"
            else:
                server['maintenance'] = False
                status = "False"
        if option.lower() == 'not_here':
            if server['not_installed'] == False:
                server['not_installed'] = True
                status = "True"
            else:
                server['not_installed'] = False
                status = "False"

        save_servers(servers)
        servers = server["name"]
        embed = msg.maitenance(servers, option, status)
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(f"Server {server} not found.", delete_after=del_time)

    await ctx.send("done", delete_after=del_time)

@bot.slash_command(
    name="add",
    description="Add a server to the database"
)
async def add_server(ctx: disnake.ApplicationCommandInteraction, name: str, ip: str):
    if ctx.author.id != you:
        await ctx.send("You are not authorized to execute this command.")
        return

    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    # Vérifier si le serveur existe déjà dans la base de données
    existing_server = next((s for s in servers if s['name'].lower() == name.lower()), None)
    if existing_server:
        await ctx.send("Server already exists in the database.")
        return

    # Ajouter le nouveau serveur à la base de données
    new_server = {
        "name": name,
        "ip": ip,
        "maintenance": False,
        "not_installed": False,
        "status": "",
        "last_status_change": 0,
        "alert": False
    }
    servers.append(new_server)
    save_servers(servers)

    embed = msg.adds(name, ip)
    await ctx.author.send(embed=embed)
    await ctx.send("done", delete_after=del_time)
    save_servers(servers)

@bot.slash_command(
    name="del",
    description="Remove a server from the database"
)
async def del_server(ctx: disnake.ApplicationCommandInteraction, name: str):
    if ctx.author.id != you:
        await ctx.send("You are not authorized to execute this command.")
        return

    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    server = next((s for s in servers if s['name'].lower() == name.lower()), None)
    ip = server["ip"]
    if server:
        servers.remove(server)
        save_servers(servers)
        embed = msg.dels(name, ip)
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(f"Server {name} not found.")
    
    await ctx.send("done", delete_after=del_time)

bot.run(token)
