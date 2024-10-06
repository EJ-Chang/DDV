import discord
import requests
from discord import app_commands
from discord.ext import commands

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

    # Get past streams (VODs)
    async def get_past_streams(self, user_id):
        url = f'https://api.twitch.tv/helix/videos?user_id={user_id}&type=archive&first=3'  # 只取最新的 3 個
        headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {TWITCH_TOKEN}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return data['data']  # 返回所有過去影片的資料
            else:
                print("No past streams found.")
                return None
        else:
            print(f"Error fetching past streams: {response.status_code}")
            return None

    # Get current stream info (title, etc.)
    async def get_twitch_stream_info(self, user_id):
        url = f'https://api.twitch.tv/helix/channels?broadcaster_id={user_id}'
        headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {TWITCH_TOKEN}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()['data']
            if data:
                return data[0]  # 返回當前直播的資料
            else:
                return None  # 用戶沒有正在直播
        else:
            print(f"Error fetching stream info: {response.status_code}")
            return None

    @app_commands.command()
    async def view(self, interaction: discord.Interaction):
        user_name = "v4181"  # Twitch ID
        user_info = await self.get_twitch_user_info(user_name)

        if user_info:
            user_id = user_info['id']
            avatar_url = user_info['profile_image_url']

            # 獲取當前直播資訊
            stream_info = await self.get_twitch_stream_info(user_id)

            embed = discord.Embed(title=f"{user_name}'s Info")
            embed.set_image(url=avatar_url)

            if stream_info:
                # 如果實況主正在直播，顯示標題
                stream_title = stream_info['title']
                embed.add_field(name="Current Stream", value=stream_title)
            else:
                embed.add_field(name="Current Stream",
                                value="Not currently streaming.")

            # 獲取過去的 VOD 資訊
            past_streams = await self.get_past_streams(user_id)
            if past_streams:
                # 顯示最新三個 VOD
                for stream in past_streams:
                    title = stream['title']
                    url = stream['url']
                    embed.add_field(name=title, value=f"[觀看連結]({url})", inline=False)

            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(
                f"Could not retrieve info for {user_name}.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Twitch_info(bot))

# memo:
# 當前直播資訊&last time stream info get
# todo:
# select streamer
