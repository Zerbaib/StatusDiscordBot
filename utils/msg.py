import disnake

def maitenance(servers, option, status):
    emd = disnake.Embed(
        title="Server config change", 
        description=f"Server configuration has been updated:\n\n"
                    f"**NAME**: {servers}\n"
                    f"**OPTION**: {option}\n"
                    f"**STATUS**: {status}",
        colour=disnake.Color.orange()
        )

    return emd

def adds(name, ip):
    emd = disnake.Embed(
        title="Server add in config", 
        description=f"Server as bin added:\n\n"
                    f"**NAME**: {name}\n"
                    f"**IP**: {ip}\n",
        colour=disnake.Color.dark_green()
        )
    
    return emd

def dels(name, ip):
    emd = disnake.Embed(
        title="Server deleted", 
        description=f"Server as bin deleted\n\n"
                    f"**NAME**: {name}\n"
                    f"**IP**: {ip}\n",
        colour=disnake.Color.dark_red()
        )
    
    return emd