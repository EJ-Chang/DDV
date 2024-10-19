import asyncio
import os
from pickle import TRUE

import discord
from discord.ext import commands
# from twitch_info import TwitchInfo  # 匯入 TwitchInfo 類別

# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

# bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    # 同步 slash 指令
    slash = await bot.tree.sync()
    print(f'Load {len(slash)} slash command(s).')
    if bot.user:
        print(f"Logged in as {bot.user.name}")
    else:
        print('Something went wrong while initiating the bot.')

    # 設定狀態為「聽音樂」
    # 目前好像只有聽(音樂) 玩(遊戲) 跟觀賞什麼可以選
    activity = discord.Activity(type=discord.ActivityType.listening,
                                name="煌Sir有汐")
    # TODO:想要 random or 跑馬燈
    await bot.change_presence(status=discord.Status.online, activity=activity)


# ADD context menu
@bot.tree.context_menu(name="Show join date")
async def get_joined_date(interaction: discord.Interaction,
                          member: discord.Member):
    if member.joined_at:
        await interaction.response.send_message(
            f'Member joined at: {discord.utils.format_dt(member.joined_at)}')
    else:
        await interaction.response.send_message('Join date unknown.')


# ADD context menu
@bot.tree.context_menu(name="Show msg create date")
async def get_message_create_date(interaction: discord.Interaction,
                                  message: discord.Message):
    if message.created_at:
        await interaction.response.send_message(
            f'This msg was created at: {discord.utils.format_dt(message.created_at)}'
        )
    else:
        await interaction.response.send_message('MSG date unknown.')


# Context menu: Message creation time
@bot.tree.context_menu(name="MSG create time")
async def get_message_create_date(interaction: discord.Interaction,
                                  message: discord.Message):
    if message.created_at:
        await interaction.response.send_message(
            f'This msg was created at: {discord.utils.format_dt(message.created_at)}'
        )
    else:
        await interaction.response.send_message('MSG date unknown.')


# Context menu: MSG time to VOD feedback
@bot.tree.context_menu(name='MSG_VOD')
async def get_msg_for_timetravel(
    interaction: discord.Interaction,
    message: discord.Message,
):
    cog = bot.get_cog('TwitchInfo')
    commands = cog.get_commands()
    print([c.name for c in commands])
    if message.created_at:
        MSG_TIME = message.created_at
        # user_name= 'seki_meridian'
        await interaction.response.send_message(
            f'MSG created at: {discord.utils.format_dt(MSG_TIME)} ')

    else:
        await interaction.response.send_message('Error in MSG VOD')


# # 在 main.py 中呼叫 TwitchInfo 的方法
# async def use_check_stream_at_time(user_id, target_time_utc):
#     # 取得 TwitchInfo cog 實例
#     cog = bot.get_cog("TwitchInfo")
#     if cog:
#         # 調用 check_stream_at_time 方法
#         vod_url, timestamp_seconds, vod_title = await cog.check_stream_at_time(
#             user_id, target_time_utc
#         )
#         print(f"VOD URL: {vod_url}, Timestamp: {timestamp_seconds}, Title: {vod_title}")
#     else:
#         print("TwitchInfo cog 未加載")

# Get token
# with open("token.txt") as file:
#   token = file.read()
token = os.environ['DISCORD_BOT_TOKEN']


# Load every cog in my cogs folder
async def Load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


# Run main script
async def main():
    async with bot:
        await Load()
        await bot.start(token)


asyncio.run(main())

# Baby DD branch
