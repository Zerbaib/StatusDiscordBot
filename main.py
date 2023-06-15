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

    server_channel = bot.get_channel(config.CHAN_ID)

    servers = config.servers

    embed_message = None

    while not bot.is_closed():
        embed = disnake.Embed(title='Status of servers')

        for server in servers:
            name = server['name']
            ip = server['ip']
            status = await ping_server(ip)

            if status == "Online":
                status = "<:on:1118875860854915152> ``Online``"
            if status == "Offline":
                status = "<:off:1118875858841649183> ``Offine``"

            embed.add_field(name=name, value=status, inline=False)

        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online !\nIf is <:idle:1118875857512038560> the server have bugs\nIf is <:off:1118875858841649183> The server is offline", inline=False)
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
