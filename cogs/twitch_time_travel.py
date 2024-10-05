import discord
import requests
from discord import app_commands
from discord.ext import commands

# Twitch API 設定
TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TWITCH_TOKEN = '9de116c56fbj6qn27ald7so9q2w5ai'
TWITCH_API_BASE_URL = 'https://api.twitch.tv/helix'

class Twitch_time_travel(commands.Cog):

  def __init__(self, bot):
      self.bot = bot



async def setup(bot):
  await bot.add_cog(Twitch_time_travel(bot))
