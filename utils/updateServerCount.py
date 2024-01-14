from disnake import Activity, ActivityType
from asyncio import sleep
from json import load

async def update_server_count(bot, sec_loop):
    while not bot.is_closed():
        with open('servers.json', 'r') as servers_file:
            servers = load(servers_file)
        servers_count = len(servers)
        activity = Activity(
            type=ActivityType.watching,
            name=f'{servers_count} servers'
        )
        await bot.change_presence(activity=activity)
        await sleep(sec_loop)