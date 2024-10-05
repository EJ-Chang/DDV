import discord
import requests
from discord import app_commands
from discord.ext import commands
import datetime

# Twitch API 設定
TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TWITCH_TOKEN = '9de116c56fbj6qn27ald7so9q2w5ai'


class SelectTwitchUser(discord.ui.Select):

    def __init__(self, bot):
        self.bot = bot

        # Twitch 選項列表
        options = [
            discord.SelectOption(label="KSP",
                                 description="Twitch ID: KSP",
                                 value="kspksp"),
            discord.SelectOption(label="Seki",
                                 description="Twitch ID: Seki",
                                 value="seki_meridian"),
            discord.SelectOption(label="Utiao",
                                 description="Twitch ID: 油條Utiao",
                                 value="v4181"),
            discord.SelectOption(label="Yuzumi",
                                 description='Twitch ID: Yuzumi',
                                 value="yuzumi_neon")
        ]

        super().__init__(placeholder="Choose a Twitch user",
                         max_values=1,
                         min_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        user_name = self.values[0]  # 選擇的 Twitch 使用者名稱
        user_info = await self.bot.get_cog('TwitchCog').get_twitch_user_basic(
            user_name)

        if user_info:
            user_id = user_info['id']
            avatar_url = user_info['profile_image_url']
            stream_info = await self.bot.get_cog(
                'TwitchCog').get_twitch_stream_info(user_id)

            # 創建一個嵌入消息，包含用戶ID和頭像
            embed = discord.Embed(title=f"Twitch User: {user_name}",
                                  color=discord.Color.random())
            # embed.add_field(name="User ID", value=user_id, inline=False)
            embed.set_thumbnail(url=avatar_url)  # 顯示用戶頭像

            if stream_info:
                stream_title = stream_info['title']
                embed.add_field(name="Stream Title",
                                value=stream_title,
                                inline=False)
            else:
                embed.add_field(name="Stream Title",
                                value="User is not streaming",
                                inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"Could not retrieve info for {user_name}.", ephemeral=True)


class SelectTwitchMenu(discord.ui.View):

    def __init__(self, bot):
        super().__init__()
        self.add_item(SelectTwitchUser(bot))


class TwitchCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Get twitch user info
    async def get_twitch_user_basic(self, user_name):
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

    # Get streams
    async def get_twitch_stream_info(self, user_id):
        url = f'https://api.twitch.tv/helix/channels?broadcaster_id={user_id}'
        headers = {
            'Client-ID': TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {TWITCH_TOKEN}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['data'][0]  # 返回用戶資料
        else:
            print(f"Error fetching stream info: {response.status_code}")
            return None

    @app_commands.command(name="select_stream",
                          description="Select a Twitch user.")
    async def select_stream(self, interaction: discord.Interaction):
        # 顯示下拉選單讓使用者選擇 Twitch 使用者
        await interaction.response.send_message("Please choose a Twitch user:",
                                                view=SelectTwitchMenu(
                                                    self.bot))


async def setup(bot):
    await bot.add_cog(TwitchCog(bot))
