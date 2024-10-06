import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View, Button


class DemoUIGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="demo_ui", description="叫出bot進行互動")
    async def demo_ui(self, interaction: discord.Interaction):
        # 創建選單
        select = Select(placeholder="選擇一個選項",
                        options=[
                            discord.SelectOption(label="A",
                                                 description="接下來請輸入文字prompt",
                                                 value="A"),
                            discord.SelectOption(label="B",
                                                 description="接下來請按按鈕",
                                                 value="B")
                        ])

        # 定義回應選單的行為
        async def select_callback(interaction: discord.Interaction):
            selected_value = select.values[0]
            if selected_value == "A":
                # 顯示月日的 slash command
                await interaction.response.send_message(
                    "請使用 `/set_date` 命令並輸入月和日", ephemeral=True)
            elif selected_value == "B":
                # 創建按鈕
                button_view = View()
                button_view.add_item(
                    Button(label="好", style=discord.ButtonStyle.success))
                button_view.add_item(
                    Button(label="壞", style=discord.ButtonStyle.danger))
                await interaction.response.send_message("請選擇按鈕：",
                                                        view=button_view,
                                                        ephemeral=True)

        # 綁定選單的回調
        select.callback = select_callback

        # 創建視圖並將選單加入視圖
        view = View()
        view.add_item(select)

        # 回應使用者，顯示選單
        await interaction.response.send_message("請從選單中選擇：",
                                                view=view,
                                                ephemeral=True)

    # 設定一個 slash command 來接收月日輸入
    @app_commands.command(name="set_date", description="輸入月日")
    @app_commands.describe(month="請輸入月份", day="請輸入日期")
    async def set_date(self, interaction: discord.Interaction, month: int,
                       day: int):
        # 可以進行格式驗證，例如檢查日期是否正確
        if 1 <= month <= 12 and 1 <= day <= 31:
            await interaction.response.send_message(f"你輸入的日期是：{month}月{day}日")
        else:
            await interaction.response.send_message("輸入的日期無效，請重新輸入！")


# 註冊bot
async def setup(bot):
    await bot.add_cog(DemoUIGame(bot))
