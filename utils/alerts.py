from utils.var import *
from disnake import Embed

def up(name):
    embed = Embed(
        title=f"END OF WARNING",
        description=f"**The server ``{name}``**\nWas **ONLINE** !",
        color=brand_green
    )
    return embed

def pending(name):
    embed = Embed(
        title=f"PENDING",
        description=f"**The server ``{name}``**\nIs **PENDING** !",
        color=dark_orange
    )
    return embed

def down(name):
    embed = Embed(
        title=f"WARNING",
        description=f"**The server ``{name}``**\nWas **OFFLINE** !",
        color=brand_red
    )
    return embed