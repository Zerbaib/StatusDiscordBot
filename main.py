import disnake
from disnake.ext import commands
import asyncio
import subprocess
import json
import os
import config

servers_file_path = 'servers.json'
if not os.path.exists(servers_file_path):
    # Créer le fichier avec une liste vide
    with open(servers_file_path, 'w') as servers_file:
        servers_file.write('[]')

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

        await asyncio.sleep(config.sec_loop)  # Attendre un certain intervalle avant la prochaine mise à jour

async def send_notification(name):
    user = await bot.fetch_user(config.YOUR_ID)

    embed = disnake.Embed(
        title="A server has gone offline",
        description=f"The server {name} is now offline.",
        color=disnake.Color.red()  # Couleur du embed (rouge dans cet exemple)
    )

    await user.send(embed=embed)

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
        return 'Erreur lors du ping', 'N/A'

async def update_servers_status():
    await bot.wait_until_ready()
    server_channel = bot.get_channel(config.CHAN_ID)
    embed_message = None

    while not bot.is_closed():
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)

        embed = disnake.Embed(title='Status of servers')
        for server in servers:
            name = server['name']
            ip = server['ip']
            maintenance = server.get('maintenance')
            not_installed = server.get('not_installed')

            if maintenance:
                status = '<:idle:1118875857512038560> ``Idle``'
                ping_result = 'N/A'
            elif not_installed:
                status = '<:no:1121213438505517197> ``Not Here``'
                ping_result = 'N/A'
            else:
                status, ping_result = await ping_server(ip)
                if status == "Online":
                    status = "<:on:1118875860854915152> ``Online``"
                else:
                    status = "<:off:1118875858841649183> ``Offline``"

                if server.get('status') == 'Online' and status == 'Offline':
                    await send_notification(name)

            embed.add_field(name=name, value=f'{status} With ``{ping_result}``', inline=False)

        if embed_message:
            embed.add_field(
                name="legend",
                value="If is <:on:1118875860854915152>, the server is online!\nIf is <:idle:1118875857512038560>, the server has bugs.\nIf is <:off:1118875858841649183>, the server is offline.\nIf is <:no:1121213438505517197>, the server is not installed",
                inline=False
            )
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        save_servers(servers)  # Save server configuration

        await asyncio.sleep(config.sec_loop)

bot.loop.create_task(update_servers_status())
bot.loop.create_task(update_server_count())

@bot.slash_command(
    name="maintenance",
    description="Enable or disable maintenance mode for a server"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, server: str, option: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("You are not authorized to execute this command.")
        return

    valid_options = ['idle', 'not_here']
    if option.lower() not in valid_options:
        await ctx.send(f"Invalid option: {option}. Valid options are: {', '.join(valid_options)}.")
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
        embed = disnake.Embed(title="Server config change", 
                              description=f"Server configuration has been updated:\n\n"
                                          f"**NAME**: {server['name']}\n"
                                          f"**OPTION**: {option}\n"
                                          f"**STATUS**: {status}"
        )
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(f"Server {server} not found.")

    await ctx.send("done", delete_after=config.del_time)

@bot.slash_command(
    name="add",
    description="Add a server to the database"
)
async def add_server(ctx: disnake.ApplicationCommandInteraction, name: str, ip: str):
    if ctx.author.id != config.YOUR_ID:
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
        "last_status_change": 0
    }
    servers.append(new_server)
    save_servers(servers)

    embed = disnake.Embed(title="Server add in config", 
                          description=f"Server as bin added:\n\n"
                                        f"**NAME**: {name}\n"
                                        f"**IP**: {ip}\n")
    await ctx.author.send(embed=embed)
    await ctx.send("done", delete_after=config.del_time)
    save_servers(servers)

@bot.slash_command(
    name="del",
    description="Remove a server from the database"
)
async def del_server(ctx: disnake.ApplicationCommandInteraction, name: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("You are not authorized to execute this command.")
        return

    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    server = next((s for s in servers if s['name'].lower() == name.lower()), None)
    ip = server["ip"]
    if server:
        servers.remove(server)
        save_servers(servers)
        embed = disnake.Embed(title="Server deleted", 
                              description=f"Server as bin deleted\n\n"
                                            f"**NAME**: {name}\n"
                                            f"**IP**: {ip}")
        await ctx.author.send(embed=embed)
    else:
        await ctx.author.send(f"Server {name} not found.")
    
    await ctx.send("done", delete_after=config.del_time)

bot.run(config.TOKEN)
