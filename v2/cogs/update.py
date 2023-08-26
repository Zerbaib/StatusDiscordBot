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

class UpdCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_file = var["SERVER_FILE"]
        self.del_time = config["del_time"]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /update has been loaded')
        print()

def setup(bot):
    bot.add_cog(UpdCommand(bot))