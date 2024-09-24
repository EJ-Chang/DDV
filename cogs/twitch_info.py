import discord
from discord.ext import commands
import requests

# Twitch API 設定
TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TWITCH_TOKEN = '9de116c56fbj6qn27ald7so9q2w5ai'


class Twitch_info(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} is online!')

  # Get info from Twitch
  async def get_twitch_user_info(self, user_name):
    url = f'https://api.twitch.tv/helix/users?login={user_name}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      return response.json()['data'][0]  # 返回用戶資料
    else:
      print(f"Error fetching user info: {response.status_code}")
      return None

  async def get_twitch_schedule(self, user_id):
    url = f'https://api.twitch.tv/helix/schedule?broadcaster_id={user_id}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      return response.json()['data']  # 返回排程資料
    else:
      print(f"Error fetching schedule: {response.status_code}")
      return None

  @commands.command()
  async def viewcarry(self, ctx):
    user_name = "carrymaybe484"  # Twitch ID
    user_info = await self.get_twitch_user_info(user_name)

    if user_info:
      user_id = user_info['id']
      avatar_url = user_info['profile_image_url']

      # 獲取排程資訊
      schedule_info = await self.get_twitch_schedule(user_id)

      embed = discord.Embed(title=f"{user_name}'s Info")
      embed.set_image(url=avatar_url)

      if schedule_info:
        # 格式化排程資訊
        schedule_text = "\n".join(f"{item['start_time']} - {item['title']}"
                                  for item in schedule_info)
        embed.add_field(name="Upcoming Schedule",
                        value=schedule_text or "No upcoming streams.")
      else:
        embed.add_field(name="Upcoming Schedule",
                        value="Could not retrieve schedule.")

      await ctx.send(embed=embed)
    else:
      await ctx.send(f"Could not retrieve info for {user_name}.")


async def setup(bot):
  await bot.add_cog(Twitch_info(bot))
