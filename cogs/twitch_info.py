import discord
import os
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import pytz  # 用來處理時區
import requests

# Twitch API 設定
# TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
# TWITCH_TOKEN = '9de116c56fbj6qn27ald7so9q2w5ai'
TWITCH_TOKEN = os.environ['TWITCH_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']


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

  # Get all past streams (VODs)
  async def get_all_past_streams(self, user_id):
    url = f'https://api.twitch.tv/helix/videos?user_id={user_id}&type=archive'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      data = response.json()
      if 'data' in data and len(data['data']) > 0:
        return data['data']  # 返回所有 VOD 的資料
      else:
        print("No past streams found.")
        return None
    else:
      print(f"Error fetching past streams: {response.status_code}")
      return None

  # 判斷特定時間是否有實況
  async def check_stream_at_time(self, user_id, target_time_utc):
    vods = await self.get_all_past_streams(user_id)

    if vods:
      for vod in vods:
        start_time_utc = datetime.fromisoformat(
            vod['created_at'][:-1]).replace(tzinfo=pytz.utc)
        duration_str = vod['duration']

        # 將持續時間轉換為 timedelta
        hours, minutes, seconds = 0, 0, 0
        time_parts = duration_str.split('h')
        if len(time_parts) == 2:
          hours = int(time_parts[0])
          duration_str = time_parts[1]
        time_parts = duration_str.split('m')
        if len(time_parts) == 2:
          minutes = int(time_parts[0])
          duration_str = time_parts[1]
        time_parts = duration_str.split('s')
        if len(time_parts) == 2:
          seconds = int(time_parts[0])

        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        end_time_utc = start_time_utc + duration

        # 判斷時間是否在直播期間
        if start_time_utc <= target_time_utc <= end_time_utc:
          # 計算時間戳記
          timestamp_seconds = int(
              (target_time_utc - start_time_utc).total_seconds())
          return vod['url'], timestamp_seconds, vod['title']

    return None, None, None

  @app_commands.command(name="time_travel", description="檢查特定時間是否有實況並返回影片連結")
  async def time_travel(self, interaction: discord.Interaction, user_name: str,
                        month: int, day: int, hour: int, minute: int):
    # 獲取當前的年份
    current_year = datetime.now().year

    # 將輸入的 GMT+8 時間轉換為 UTC
    local_tz = pytz.timezone('Asia/Taipei')
    local_time = local_tz.localize(
        datetime(current_year, month, day, hour, minute))
    target_time_utc = local_time.astimezone(pytz.utc)

    user_info = await self.get_twitch_user_info(user_name)

    if user_info:
      user_id = user_info['id']
      avatar_url = user_info['profile_image_url']

      # 檢查該時間是否有實況
      vod_url, timestamp_seconds, vod_title = await self.check_stream_at_time(
          user_id, target_time_utc)

      embed = discord.Embed(title=f"{user_name}'s Info")
      embed.set_image(url=avatar_url)

      # 新增查詢時間的顯示
      query_time = f"{month}月{day}日 {hour}點{minute}分"
      embed.add_field(name="查詢時間", value=f"你查詢的是 {query_time}", inline=False)

      if vod_url:
        # 返回帶時間戳的影片連結和 VOD 標題
        timestamp_url = f"{vod_url}?t={timestamp_seconds}s"
        embed.add_field(name="Stream Status",
                        value=f"當時有實況，這是對應的 [影片連結]({timestamp_url})",
                        inline=False)
        embed.add_field(name="VOD Title", value=f"{vod_title}", inline=False)
      else:
        embed.add_field(name="Stream Status",
                        value="在該時間沒有實況進行。",
                        inline=False)

      await interaction.response.send_message(embed=embed)

    else:
      await interaction.response.send_message(f"無法取得 {user_name} 的資訊。",
                                              ephemeral=True)


async def setup(bot):
  await bot.add_cog(Twitch_info(bot))


# memo:
# 當前直播資訊&last time stream info get
# todo:
# select streamer
