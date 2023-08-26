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

class AddCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_file = var["SERVER_FILE"]
        self.del_time = config["del_time"]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /add has been loaded')
        print()

    @commands.slash_command(
        name="add",
        description="Add a server to the database"
    )
    @commands.is_owner()
    async def add_server(self, ctx: disnake.ApplicationCommandInteraction, name: str, ip: str):
        with open('servers.json', 'r') as servers_file:
            servers = json.load(servers_file)

        # Vérifier si le serveur existe déjà dans la base de données
        existing_server = next((s for s in servers if s['name'].lower() == name.lower()), None)
        if existing_server:
            await ctx.send("Server already exists in the database.")
            return

        # Ajouter le nouveau serveur à la base de données
        new_server = {
            "name": name,
            "ip": ip,
            "maintenance": False,
            "not_installed": False,
            "status": "",
            "last_status_change": 0,
            "alert": False
        }
        servers.append(new_server)
        save_servers(servers)

        embed = msg.adds(name, ip)
        await ctx.author.send(embed=embed)
        await ctx.send("done", delete_after=self.del_time)
        save_servers(servers)

def setup(bot):
    bot.add_cog(AddCommand(bot))