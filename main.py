import disnake
from disnake.ext import commands
import asyncio
import subprocess
import json
import config

# Charger la configuration depuis le fichier JSON
with open('servers.json', 'r') as servers_file:
    servers = json.load(servers_file)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
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
    description="Active ou désactive la maintenance pour un serveur"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, serveur: str):
    if ctx.author.id != config.YOUR_ID:
        await ctx.send("Vous n'êtes pas autorisé à exécuter cette commande.")
        return

    server = next((s for s in servers if s['name'].lower() == serveur.lower()), None)

    if server:
        server['maintenance'] = not server['maintenance']
        save_servers()  # Sauvegarder la configuration des serveurs
        await ctx.send(f"Le serveur {server['name']} est maintenant en maintenance : {server['maintenance']}")
    else:
        await ctx.send("Serveur introuvable")

async def update_servers_status():
    await bot.wait_until_ready()

    server_channel = bot.get_channel(config.CHAN_ID)
    embed_message = None

    while not bot.is_closed():
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

            server['status'] = status  # Mettre à jour l'état du serveur dans la configuration

            # Calculer la durée d'état
            if 'last_status_change' not in server:
                server['last_status_change'] = asyncio.get_event_loop().time()

            current_time = asyncio.get_event_loop().time()
            elapsed_time = current_time - server['last_status_change']
            server['last_status_change'] = current_time

            embed.add_field(name=name, value=f'{status}\n*(Depuis {elapsed_time:.2f} secondes)*', inline=False)

        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online !\nIf is <:idle:1118875857512038560> the server have bugs\nIf is <:off:1118875858841649183> The server is offline", inline=False)
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        save_servers()  # Sauvegarder la configuration des serveurs

        await asyncio.sleep(60)

bot.loop.create_task(update_servers_status())
bot.run(config.TOKEN)
