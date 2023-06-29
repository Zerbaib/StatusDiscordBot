import disnake

def shutdown(name):
    embed = disnake.Embed(
        title=f"WARNING",
        description=f"**The server ``{name}``**\nWas **OFFLINE** !",
        color=disnake.Color.red()  # Couleur du embed (rouge dans cet exemple)
    )
    return embed

def boot(name):
    embed = disnake.Embed(
        title=f"END OF WARNING",
        description=f"**The server ``{name}``**\nWas **ONLINE** !",
        color=disnake.Color.green()  # Couleur du embed (rouge dans cet exemple)
    )
    return embed