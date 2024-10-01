import discord
from discord import app_commands
from discord.ext import commands


class Dc_handler(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{__name__} is online!')

  # @app_commands.command(name='greet', description='Greet the user.')
  # async def greet(self, interaction: discord.Interaction):
  #   response = 'Hello, I am your discord bot'
  #   await interaction.response.send_message(response)


async def setup(bot):
  await bot.add_cog(Dc_handler(bot))
