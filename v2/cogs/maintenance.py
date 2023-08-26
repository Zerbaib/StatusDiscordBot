import disnake
from disnake.ext import commands
from utils import msg
import json

with open("utils/var.json", "r") as var_file:
    var = json.load(var_file)
with open(var["CONFIG_FILE"], "r") as conf_file:
    config = json.load(conf_file)    

def save_servers(servers):
    with open(var["SERVER_FILE"], 'w') as servers_file:
        json.dump(servers, servers_file, indent=4, ensure_ascii=False)

class MtnCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_file = var["SERVER_FILE"]
        self.del_time = config["del_time"]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /maintenance has been loaded')
        print()

    @commands.slash_command(
        name="maintenance",
        description="Enable or disable maintenance mode for a server"
    )
    @commands.is_owner()
    async def maintenance(self, ctx: disnake.ApplicationCommandInteraction, server: str, option: str):

        valid_options = ['idle', 'not_here']
        if option.lower() not in valid_options:
            embed = disnake.Embed(title="Invalid option !", 
                                description=f"Only 2 option is possible:\n\n"
                                            f"**For orange mode:**```idle```\n"
                                            f"**For grey mode:**```not_here```",
                                color=disnake.Color.red())
            await ctx.send(embed=embed, delete_after=self.del_time)
            return

        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)

        server = next((s for s in servers if s['name'].lower() == server.lower()), None)

        if server:
            if option.lower() == 'idle':
                if server['maintenance'] == False:
                    server['maintenance'] = True
                    status = "True"
                else:
                    server['maintenance'] = False
                    status = "False"
            if option.lower() == 'not_here':
                if server['not_installed'] == False:
                    server['not_installed'] = True
                    status = "True"
                else:
                    server['not_installed'] = False
                    status = "False"

            save_servers(servers)
            servers = server["name"]
            embed = msg.maitenance(servers, option, status)
            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send(f"Server {server} not found.", delete_after=self.del_time)

        await ctx.send("done", delete_after=self.del_time)

def setup(bot):
    bot.add_cog(MtnCommand(bot))