import discord
from discord.ext import commands
from discord import app_commands


class SelectTwitchUser(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        # Twitch 選項列表
        options = [
            discord.SelectOption(label="KSP", description="Twitch ID: KSP", value="kspksp"),
            discord.SelectOption(label="Seki", description="Twitch ID: Seki", value="seki_meridian"),
            discord.SelectOption(label="Utiao", description="Twitch ID: 油條Utiao", value="v4181"),
            discord.SelectOption(label="Yuzumi", description='Twitch ID: Yuzumi', value="yuzumi_neon")
        ]

        super().__init__(placeholder="Choose a Twitch user", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user_name = self.values[0]  # 選擇的 Twitch 使用者名稱
        await interaction.response.defer()  # 延遲回應，以便處理後續的邏輯

        # 獲取 Twitch 使用者資訊
        user_info = await self.bot.get_twitch_user_info(user_name)

        if user_info:
            user_id = user_info['id']
            avatar_url = user_info['profile_image_url']

            # 獲取當前直播資訊
            stream_info = await self.bot.get_twitch_stream_info(user_id)

            # 建立嵌入消息
            embed = discord.Embed(title=f"{user_name}'s Info")
            embed.set_image(url=avatar_url)

            if stream_info:
                stream_title = stream_info['title']
                embed.add_field(name="Current Stream", value=stream_title)
            else:
                embed.add_field(name="Current Stream", value="Not currently streaming.")

            # 獲取過去直播
            past_streams = await self.bot.get_past_streams(user_id)
            if past_streams:
                embed.add_field(name="Schedule", value=past_streams)

            # 發送嵌入消息
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"Could not retrieve info for {user_name}.")


class SelectTwitchMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(SelectTwitchUser(bot))


class TwitchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="view", description="View a Twitch user's info.")
    async def view(self, interaction: discord.Interaction):
        # 顯示下拉選單讓使用者選擇 Twitch 使用者
        await interaction.response.send_message("Please choose a Twitch user:", view=SelectTwitchMenu(self.bot))

async def setup(bot):
    await bot.add_cog(TwitchCog(bot))