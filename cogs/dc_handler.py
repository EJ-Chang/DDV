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
  @app_commands.command(name="fetch_replied_message", description="Fetch the message you replied to.")
  async def fetch_replied_message(self, interaction: discord.Interaction):
    # 檢查使用者是否回覆了某條消息
    if interaction.message and interaction.message.reference:
        # 獲取被回覆的消息
        replied_message_id = interaction.message.reference.message_id
        channel = interaction.channel

        try:
            # 根據消息 ID 抓取消息
            replied_message = await channel.fetch_message(replied_message_id)

            # 發送回覆消息的內容與發送時間
            await interaction.response.send_message(
                f"Replied message content: {replied_message.content}\n"
                f"Sent at: {replied_message.created_at}"
            )
        except discord.NotFound:
            await interaction.response.send_message("The replied message was not found.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to fetch that message.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Failed to fetch the message due to an HTTP error.", ephemeral=True)
    else:
        await interaction.response.send_message("You did not reply to any message.", ephemeral=True)

async def setup(bot):
  await bot.add_cog(Dc_handler(bot))
