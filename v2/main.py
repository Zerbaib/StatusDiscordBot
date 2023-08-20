import os
import json
import platform
import aiohttp
import disnake
from disnake.ext import commands

with open("utils/var.json", "r") as var_file:
    var = json.load(var_file)    

config_file_path = var["CONFIG_FILE"]
srv_data_file_path = var["SERVER_FILE"]
online_version = var["ONLINE_VER"]

if not os.path.exists(srv_data_file_path):
    with open(srv_data_file_path, 'w') as server_file:
        json.dump({}, server_file)

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token:\n")
        prefix = input("Enter the bot's prefix:\n")
        chan_id = int(input("Enter the id of the status channel:\n"))
        you_id = int(input("Enter your Discord ID:\n"))
        loop = int(input("Enter the time of the refresh loop in second (min 5s):\n"))
        if loop <= 5 :
            old_loop = loop
            loop = 5
            print(f"You can set [ {old_loop} ] is now -> {loop}")
        config_data = {
                "TOKEN": token,
                "PREFIX": prefix,
                "CHAN_ID": chan_id,
                "MSG_ID": None,
                "YOUR_ID": you_id,
                "sec_loop": 60,
                "del_time": 3
        }
        json.dump(config_data, config_file, indent=4)
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

bot = commands.Bot(
    command_prefix=config["PREFIX"],
    intents=disnake.Intents.all(),
    case_insensitive=True
)

bot.remove_command('help')

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    async with aiohttp.ClientSession() as session:
        async with session.get(online_version) as response:
            if response.status == 200:
                bot_repo_version = await response.text()
            else:
                bot_repo_version = "Unknown"

    with open(var["LOCAL_VER"], 'r') as version_file:
        bot_version = version_file.read().strip()

    if bot_version != bot_repo_version:
        print()
        print('===============================================')
        print('🛑 You are not using the latest version!')
        print('🛑 Please update the bot.')
        print('🛑 Use "git fetch && git pull" to update your bot.')
    print('===============================================')
    print(f"🔱 The bot is ready!")
    print(f'🔱 Logged in as {nbot} | {bot.user.id}')
    print(f'🔱 Bot local version: {bot_version}')
    print(f'🔱 Bot online version: {bot_repo_version}')
    print(f"🔱 Disnake version: {disnake.__version__}")
    print(f"🔱 Running on {platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Python version: {platform.python_version()}")
    print('===============================================')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'cogs.{cog_name}')
        except Exception as e:
            print(f"🌪️  Error during '{cog_name}' loading:\n\n{e}")

bot.run(config["TOKEN"])