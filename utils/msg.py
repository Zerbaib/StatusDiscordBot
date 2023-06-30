import disnake

def maitenance(servers, option, status):
    emd = disnake.Embed(
        title="Server config change", 
        description=f"Server configuration has been updated:\n\n"
                    f"**NAME**: {servers}\n"
                    f"**OPTION**: {option}\n"
                    f"**STATUS**: {status}"
        )
    if option == "idle":
        emd.colour = disnake.Color.dark_orange()
    else:
        emd.colour = disnake.Color.dark_grey()