import disnake
from disnake.ext import commands
import asyncio
import subprocess
import config
import datetime
import json
bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
@bot.event
async def update_servers_status():
    await bot.wait_until_ready()
    server_channel = bot.get_channel(config.CHAN_ID)
    embed_message = None
    while not bot.is_closed():
        servers = config.servers
        embed = disnake.Embed(title='Status of servers')
        for server in servers:
            name = server['name']
            ip = server['ip']
            maintenance = server['maintenance']
            last_updated = server.get('last_updated', None)
            
            if maintenance:
                status = '<:idle:1118875857512038560> Idle'
            else:
                status = await ping_server(ip)
            if status == "Online":
                status = "<:on:1118875860854915152> ``Online``"
            if status == "Offline":
                status = "<:off:1118875858841649183> ``Offine``"
            embed.add_field(name=name, value=status, inline=False)
            if last_updated:
                time_delta = datetime.datetime.now() - last_updated
                embed.add_field(name="Time Since Last Update", value=str(time_delta))
            if status != server['status'] or maintenance != server['maintenance']:
                server['status'] = status
                server['maintenance'] = maintenance
                server['last_updated'] = datetime.datetime.now()
                save_config()
        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online !\nIf is <:idle:1118875857512038560> the server have bugs\nIf is <:off:1118875858841649183> The server is offline", inline=False)
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        await asyncio.sleep(60)
        await asyncio.sleep(config.sec_loop)

async def ping_server(ip):
    try:
        # Execute a ping command
        result = await asyncio.create_subprocess_shell(
            f'ping -c 1 {ip}', stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await result.communicate()
        if result.returncode == 0:
            return 'Online'
        else:
            return 'Offline'
    except Exception:
        return 'Error while pinging'
def save_config():
    with open('config.py', 'w') as config_file:
        json.dump(config.servers, config_file)
@bot.slash_command(
    name="maintenance",
    description="Activate or deactivate maintenance mode for a server"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, serveur: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("You are not authorized to execute this command.")
        return
    server = next((s for s in config.servers if s['name'].lower() == serveur.lower()), None)
    if server:
        server['maintenance'] = not server['maintenance']
        server['last_updated'] = datetime.datetime.now()
        save_config()
        await ctx.send(f"The server {server['name']} is now in maintenance: {server['maintenance']}")
    else:
        await ctx.send("Server not found")
bot.loop.create_task(update_servers_status())
bot.run(config.TOKEN)