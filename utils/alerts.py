from utils.var import *

def up(name):
    embed = disnake.Embed(
        title=f"END OF WARNING",
        description=f"**The server ``{name}``**\nWas **ONLINE** !",
        color=brand_green
    )
    return embed

def pending(name):
    embed = disnake.Embed(
        title=f"PENDING",
        description=f"**The server ``{name}``**\nIs **PENDING** !",
        color=brand_orange
    )
    return embed

def down(name):
    embed = disnake.Embed(
        title=f"WARNING",
        description=f"**The server ``{name}``**\nWas **OFFLINE** !",
        color=brand_red
    )
    return embed