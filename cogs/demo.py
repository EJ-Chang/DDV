import discord
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
    # 先用 button 選要哪個功能的示範
    # 按照選項，提供相對應的 embed message
    @app_commands.command(name="demo_ddv", description="DDV 的功能示範")
    async def demo_ddv(self, interaction: discord.Interaction):

        # write my embed message here (demo message)
        embed = discord.Embed(title="DEMO")
        embed.add_field(name="Demo: /time_travel",
                        value="time travel 示範blahblah")

        await interaction.response.send_message(embed=embed)


# 將這個 cog 加入到 bot 裡面
async def setup(bot):
    await bot.add_cog(Demo(bot))
