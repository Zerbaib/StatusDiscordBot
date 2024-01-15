from utils.var import *
from utils.sql import create_database
from utils.alerts import *
from utils.updateServerCount import update_server_count
from disnake import Intents, NotFound, Embed
from disnake.ext import commands
from asyncio import sleep
import aioping
from json import load, dump
from os import path, listdir

if not path.exists(database_path):
    create_database(database_path)

if not path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        dump(config_data, config_file, indent=4)

with open(config_file_path, 'r') as config_file:
    config = load(config_file)

token = config["TOKEN"]
chan = config["CHAN_ID"]
you = config["YOUR_ID"]
sec_loop = config["sec_loop"]
del_time = config["del_time"]

bot = commands.Bot(command_prefix='!', intents=Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

for filename in listdir(cogs_dir):
    if filename.endswith('.py'):
        cog = f'{cogs_dir}.{filename[:-3]}'
        bot.load_extension(cog)
        print(f'Loaded {cog}')

bot.run(token)
