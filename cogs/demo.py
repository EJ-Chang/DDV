import os
import discord

import requests
from discord import app_commands
from discord.ext import commands

# cog: 創造 Demo 
class Demo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # listen to this cog
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is online!')
    # app commands in this cog
    @app_commands.command(name="bot_demo", description="DDV 的功能示範")
    async def bot_demo(self, interaction:discord.Interaction):
        # write my embed message here (demo message)
        embed = discord.Embed(title="DEMO")
        embed.add_field(name="Demo: /time_travel", value="time travel 示範blahblah")

        await interaction.response.send_message(embed=embed)


# 將這個 cog 加入到 bot 裡面
async def setup(bot):
    await bot.add_cog(Demo(bot))

