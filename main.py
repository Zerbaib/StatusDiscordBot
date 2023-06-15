import disnake
from disnake.ext import commands
import asyncio
import subprocess
import config

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(
        servers = 0
        for servers in config.servers:
            servers += 1
        activity=disnake.Activity(
            type=disnake.ActivityType.watching,
            name=f'{servers} servers'
        )
    )
    print(f'Logged in as {bot.user.name} ✅')

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
            
            if maintenance:
                status = '<:idle:1118875857512038560> ``Idle``'
            else:
                status = await ping_server(ip)

            if status == "Online":
                status = "<:on:1118875860854915152> ``Online``"
            if status == "Offline":
                status = "<:off:1118875858841649183> ``Offine``"

            embed.add_field(name=name, value=status, inline=False)

        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online.\nIf is <:idle:1118875857512038560> is in maintenance.\nIf is <:off:1118875858841649183> is offline.", inline=False)
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        await asyncio.sleep(config.sec_loop)

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

@bot.slash_command(
    name="maintenance",
    description="Active/désactive la maintenance"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, serveur: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("Vous n'êtes pas autorisé à exécuter cette commande.")
        return

    server = next((s for s in config.servers if s['name'].lower() == serveur.lower()), None)

    if server:
        server['maintenance'] = not server['maintenance']
        await ctx.send(f"Le serveur {server['name']} est maintenant en maintenance : {server['maintenance']}")
    else:
        await ctx.send("Serveur introuvable")

bot.loop.create_task(update_servers_status())
bot.run(config.TOKEN)
