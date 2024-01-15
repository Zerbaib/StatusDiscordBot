from utils.sql import add_data, create_table, check_data_exist, check_table_exist
from utils.var import *
from utils.json import get_data

from disnake import Embed
from disnake.ext import commands

class AddCMD(commands.Cog):
    def __init__(self, bot):
        self.config = get_data(config_file_path)
        self.bot = bot
        self.you = self.config["YOUR_ID"]

    @commands.slash_command(name="add", description="Add a server to the database")
    async def add(self, ctx, ip, name):
        if ctx.author.id != self.you:
            Embed(title="You are not authorized to execute this command.", color=brand_red)
            return
        
        if not check_table_exist(database_path, "servers"):
            create_table(database_path, "servers", ["ip", "name", "status", "maintenence"])
        
        status = "None"
        maintenence = "None"
        
        if check_data_exist(database_path, "servers", ip):
            Embed(title="This server is already in the database.", color=brand_red)
            return
        else:
            add_data(database_path, "servers", (ip, name, status, maintenence))
            Embed(title="Server added to the database.", color=brand_green)
            return

def setup(bot):
    bot.add_cog(AddCMD(bot))
