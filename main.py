import disnake
from disnake.ext import commands
import asyncio
import subprocess
import json
import config

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

servers = []  # Variable globale pour stocker les informations des serveurs

@bot.event
async def on_ready():
    global servers  # Déclarer la variable 'servers' en tant que variable globale

    # Load the configuration from the JSON file
    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    servers_count = len(servers)
    await bot.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f'{servers_count} servers'
        )
    )
    print(f'Logged in as {bot.user.name}')

def save_servers():
    with open('servers.json', 'w') as servers_file:
        json.dump(servers, servers_file, indent=4)

async def ping_server(ip):
    try:
        result = await asyncio.create_subprocess_shell(
            f'ping -c 1 {ip}', stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await result.communicate()
        if result.returncode == 0:
            return 'Online'
        else:
            return 'Offline'
    except Exception:
        return 'Erreur lors du ping'

async def update_servers_status():
    await bot.wait_until_ready()
    server_channel = bot.get_channel(config.CHAN_ID)
    embed_message = None
    
    while not bot.is_closed():
        # Load the configuration from the JSON file
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)
        
        embed = disnake.Embed(title='Status of servers')
        for server in servers:
            name = server['name']
            ip = server['ip']
            maintenance = server['maintenance']
            
            if maintenance:
                status = '<:idle:1118875857512038560> ``Idle``'
            else:
                status = await ping_server(ip)
            
            if status == "Online":
                status = "<:on:1118875860854915152> ``Online``"
            if status == "Offline":
                status = "<:off:1118875858841649183> ``Offline``"
            
            server['status'] = status  # Update server status in the configuration
            
            # Calculate status duration
            if 'last_status_change' not in server:
                server['last_status_change'] = asyncio.get_event_loop().time()
            current_time = asyncio.get_event_loop().time()
            elapsed_time = current_time - server['last_status_change']
            server['last_status_change'] = current_time
            
            embed.add_field(name=name, value=f'{status}\n*(For {elapsed_time:.2f} seconds)*', inline=False)

        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online!\nIf is <:idle:1118875857512038560> the server has bugs\nIf is <:off:1118875858841649183> The server is offline", inline=False)
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        save_servers()  # Save server configuration

        await asyncio.sleep(config.sec_loop)

bot.loop.create_task(update_servers_status())

@bot.slash_command(
    name="maintenance",
    description="Enable or disable maintenance mode for a server"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, server: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("You are not authorized to execute this command.")
        return

    server = next((s for s in servers if s['name'].lower() == server.lower()), None)

    if server:
        server['maintenance'] = not server['maintenance']
        save_servers()  # Save server configuration
        await ctx.author.send(f"The server {server['name']} is now in maintenance mode: {server['maintenance']}")
    else:
        await ctx.author.send("Server not found")

bot.run(config.TOKEN)
