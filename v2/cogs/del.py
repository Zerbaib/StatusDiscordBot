import disnake
from disnake.ext import commands
import json

with open("utils/var.json", "r") as var_file:
    var = json.load(var_file)
with open(var["CONFIG_FILE"], "r") as conf_file:
    config = json.load(conf_file)    

class DelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_file = var["SERVER_FILE"]
        self.del_time = config["del_time"]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /del has been loaded')
        print()

    @commands.slash_command(
    name="del",
    description="Remove a server from the database"
    )
    @commands.is_owner()
    async def del_server(self, ctx: disnake.ApplicationCommandInteraction, name: str):
        with open(var["SERVER_FILE"], 'r') as servers_file:
            servers = json.load(servers_file)

        server = next((s for s in servers if s['name'].lower() == name.lower()), None)
        ip = server["ip"]
        if server:
            servers.remove(server)
            save_servers(servers)
            embed = msg.dels(name, ip)
            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send(f"Server {name} not found.")
        
        await ctx.send("done", delete_after=self.del_time)

def setup(bot):
    bot.add_cog(DelCommand(bot))