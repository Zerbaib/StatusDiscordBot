import disnake
from disnake.ext import commands
import asyncio
import subprocess
import config

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def update_servers_status():
    await bot.wait_until_ready()

    server_channel_id = 1234567890  # ID du canal où vous souhaitez envoyer l'embed
    server_channel = bot.get_channel(server_channel_id)

    servers = [
        {'name': 'Serveur 1', 'ip': '127.0.0.1'},
        {'name': 'Serveur 2', 'ip': '192.168.0.1'},
        {'name': 'Serveur 3', 'ip': 'example.com'},
    ]

    embed_message = None

    while not bot.is_closed():
        embed = disnake.Embed(title='État des serveurs')

        for server in servers:
            name = server['name']
            ip = server['ip']
            status = await ping_server(ip)

            embed.add_field(name=name, value=status, inline=True)

        if embed_message:
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        await asyncio.sleep(60)

async def ping_server(ip):
    try:
        # Exécute une commande ping
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

bot.loop.create_task(update_servers_status())
bot.run(config.TOKEN)
