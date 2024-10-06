import discord
import requests
import json
import os
from discord.ext import commands
from discord import app_commands

# Twitch API 設定
# TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
# TWITCH_TOKEN = '9de116c56fbj6qn27ald7so9q2w5ai'
TWITCH_TOKEN = os.environ['TWITCH_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']


# 讀取 JSON 檔案中的實況主資料
def load_streamer_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)['streamers']


# 將 HEX 顏色轉換為 Discord 支持的顏色格式
def hex_to_rgb_int(hex_color):
    hex_color = hex_color.lstrip('#')  # 移除 #
    return int(hex_color, 16)  # 將HEX轉為整數


class SelectTwitchUser(discord.ui.Select):

    def __init__(self, bot, streamer_data):
        self.bot = bot
        self.streamer_data = {
            streamer['twitch_name']: streamer
            for streamer in streamer_data
        }

        # 根據 streamer_data 動態生成 Twitch 選項列表
        options = [
            discord.SelectOption(
                label=streamer['name'],
                description=f"Twitch ID: {streamer['twitch_name']}",
                value=streamer['twitch_name'],
            ) for streamer in streamer_data
        ]

        super().__init__(placeholder="Choose a Twitch user",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        user_name = self.values[0]  # 選擇的 Twitch 使用者名稱
        user_info = await self.bot.get_cog('TwitchCog').get_twitch_user_info(
            user_name)

        if user_info:
            user_id = user_info['id']
            avatar_url = user_info['profile_image_url']

            # 從 streamer_data 中獲取對應的代表色
            streamer = self.streamer_data.get(user_name)
            embed_color = hex_to_rgb_int(
                streamer['hex_color']) if streamer else discord.Color.random()

            # 創建嵌入消息，包含用戶ID和頭像，並使用代表色
            embed = discord.Embed(title=f"Twitch User: {user_name}",
                                  color=embed_color)
            embed.set_thumbnail(url=avatar_url)  # 顯示用戶頭像

            # 獲取最近3個VOD
            past_3_streams = await self.bot.get_cog(
                'TwitchCog').get_latest_3_streams(user_id)
            if past_3_streams:
                for stream in past_3_streams:
                    title = stream['title']
                    vod_url = stream['url']
                    embed.add_field(name=f"VOD Title",
                                    value=f"[{title}]({vod_url})",
                                    inline=False)

                await interaction.response.send_message(embed=embed)
            else:
                embed.add_field(name="VOD Status",
                                value="No recent VODs found.",
                                inline=False)
                await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(
                f"Could not retrieve info for {user_name}.", ephemeral=True)


class SelectTwitchMenu(discord.ui.View):

    def __init__(self, bot, streamer_data):
        super().__init__()
        self.add_item(SelectTwitchUser(bot, streamer_data))


class TwitchCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Get twitch user info
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

    # Get latest 3 VODs
    async def get_latest_3_streams(self, user_id):
        url = f'https://api.twitch.tv/helix/videos?user_id={user_id}&type=archive'
        headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {TWITCH_TOKEN}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                return data['data'][:3]  # 只返回最近3個VOD
            else:
                print("No past streams found.")
                return None
        else:
            print(f"Error fetching past streams: {response.status_code}")
            return None

    # Define slash command
    @app_commands.command(name="select_stream",
                          description="Select a Twitch user.")
    async def select_stream(self, interaction: discord.Interaction):
        # 讀取實況主資料
        streamer_data = load_streamer_data('streamers.json')
        # 顯示下拉選單讓使用者選擇 Twitch 使用者
        await interaction.response.send_message("Please choose a Twitch user:",
                                                view=SelectTwitchMenu(
                                                    self.bot, streamer_data))


async def setup(bot):
    await bot.add_cog(TwitchCog(bot))
