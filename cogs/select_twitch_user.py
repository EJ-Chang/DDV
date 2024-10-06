import discord
import requests
from discord.ext import commands
from discord import app_commands

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
                                 description="Twitch ID: Yuzumi",
                                 value="yuzumi_neon"),
            discord.SelectOption(label="OW2",
                                 description="Twitch ID: Overwatch Esports",
                                 value="ow_esports")
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

            # 創建嵌入消息，包含用戶ID和頭像
            embed = discord.Embed(title=f"Twitch User: {user_name}",
                                  color=discord.Color.random())
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

    def __init__(self, bot):
        super().__init__()
        self.add_item(SelectTwitchUser(bot))


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
        # 顯示下拉選單讓使用者選擇 Twitch 使用者
        await interaction.response.send_message("Please choose a Twitch user:",
                                                view=SelectTwitchMenu(
                                                    self.bot))


async def setup(bot):
    await bot.add_cog(TwitchCog(bot))
