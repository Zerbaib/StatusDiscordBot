import disnake
from disnake.ext import commands
import asyncio
import subprocess
import json
import config

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

@bot.event
async def on_ready():
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

def save_servers(servers):
    with open('servers.json', 'w') as servers_file:
        json.dump(servers, servers_file, indent=4, ensure_ascii=False)

async def ping_server(ip):
    try:
        result = await asyncio.create_subprocess_shell(
            f'ping -c 1 {ip}', stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, _ = await result.communicate()
        output = output.decode('utf-8')
        if result.returncode == 0:
            # Extraire le temps de ping de la sortie
            start_index = output.find('time=')
            if start_index != -1:
                end_index = output.find(' ms', start_index)
                if end_index != -1:
                    ping_time = output[start_index + 5:end_index]
                    return f'{ping_time} ms'
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
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)
        
        embed = disnake.Embed(title='Status of servers')
        for server in servers:
            name = server['name']
            ip = server['ip']
            maintenance = server.get('maintenance')
            ping_result = ""  # Déplacer l'initialisation ici

            if maintenance:
                status = '<:idle:1118875857512038560> ``Idle``'
            else:
                status = await ping_server(ip)
                if status == "Online":
                    status = "<:on:1118875860854915152> ``Online``"
                    ping_result = await ping_server(ip)  # Assigner la valeur ici
                    if ping_result.startswith("Erreur"):
                        status = "<:error:YOUR_ERROR_EMOJI_ID> ``Error``"
                else:
                    status = "<:off:1118875858841649183> ``Offline``"
            
            embed.add_field(name=name, value=f'{status} With ``{ping_result}``', inline=False)

        if embed_message:
            embed.add_field(name="legend", value="If is <:on:1118875860854915152> Is online!\nIf is <:idle:1118875857512038560> the server has bugs\nIf is <:off:1118875858841649183> The server is offline", inline=False)
            await embed_message.edit(embed=embed)
        else:
            embed_message = await server_channel.send(embed=embed)

        save_servers(servers)  # Save server configuration

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

    with open('servers.json', 'r') as servers_file:
        servers = json.load(servers_file)

    server = next((s for s in servers if s['name'].lower() == server.lower()), None)

    if server:
        server['maintenance'] = not server.get('maintenance', False)
        save_servers(servers)
        await ctx.author.send(f"Maintenance mode for {server['name']} has been {'enabled' if server['maintenance'] else 'disabled'}.")
    else:
        await ctx.author.send(f"Server {server} not found.")
    
    await ctx.send("done", delete_after=config.del_time)

bot.run(config.TOKEN)
