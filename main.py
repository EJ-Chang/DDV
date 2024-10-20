import asyncio
import os

import discord
from discord.ext import commands

import utils

# Twitch API 設定
TWITCH_TOKEN = os.environ['TWITCH_TOKEN']
TWITCH_CLIENT_ID = os.environ['TWITCH_CLIENT_ID']

# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


# Load every cog in my cogs folder
async def Load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


# 定義要輪流顯示的狀態
STATUS_LIST = ["Playing Minecraft", "Coding a Discord Bot", "/demo & 新功能"]


async def cycle_status():
    """每隔幾秒自動更換 Bot 的狀態。"""
    while True:
        for status in STATUS_LIST:
            # 設置 Bot 的狀態
            activity = discord.Game(name=status)
            await bot.change_presence(activity=activity)

            # 每隔 30 秒切換一次狀態
            await asyncio.sleep(30)


@bot.event
async def on_ready():
    # 同步 slash 指令
    slash = await bot.tree.sync()
    print(f'Load {len(slash)} slash command(s).')
    if bot.user:
        print(f"Logged in as {bot.user.name}")
    else:
        print('Something went wrong while initiating the bot.')
    # 啟動狀態切換協程
    bot.loop.create_task(cycle_status())


# Context menu: MSG time to VOD feedback
@bot.tree.context_menu(name="[SEKI] 查詢此刻 SEKI 的台")
async def get_msg_for_timetravel_at_seki(interaction: discord.Interaction,
                                         message: discord.Message):

    user_name = 'seki_meridian'
    user_info = await utils.get_twitch_user_info(user_name)
    target_time_utc = utils.discord_to_twitch_datetime(message.created_at)

    if user_info:
        user_id = user_info['id']
        avatar_url = user_info['profile_image_url']
        # 檢查該時間是否有實況
        vod_url, timestamp_seconds, vod_title = await utils.check_stream(
            user_id, target_time_utc) or (None, None, None)

        # embed = discord.Embed(title=f"{user_name}'s Info")
        # embed.set_thumbnail(url=avatar_url)

        # embed = discord.Embed(title=f"{user_name}'s Info")
        # embed.add_field(name='UserID is:', value=f'{user_id}')
        # embed.add_field(name='查詢的時間是:', value=f'{target_time_utc}')
        # # embed.add_field(name='URL', value= vod_url)
        # if vod_url:
        #     # 返回帶時間戳的影片連結和 VOD 標題
        #     timestamp_url = f"{vod_url}?t={timestamp_seconds}s"
        #     embed.add_field(name="Stream Status", value="當時有開台", inline=False)
        #     embed.add_field(name="實況連結(帶有時間戳記)",
        #                     value=f"[{vod_title}]({timestamp_url})",
        #                     inline=False)
        # else:
        #     embed.add_field(name="Stream Status", value="當時沒有開台", inline=False)

        # # await interaction.response.send_message(embed=embed)
        # embed.set_thumbnail(url=avatar_url)
        # 使用模組化的 embed 函數
        embed = utils.create_vod_embed(user_name, user_id, avatar_url,
                                       target_time_utc, vod_url,
                                       timestamp_seconds, vod_title)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message('not working', ephemeral=True)


# Context menu: MSG time to VOD feedback
@bot.tree.context_menu(name="[KSP] 查詢此刻 KSP 的台")
async def get_msg_for_timetravel_at_ksp(interaction: discord.Interaction,
                                        message: discord.Message):

    user_name = 'kspksp'
    user_info = await utils.get_twitch_user_info(user_name)
    target_time_utc = utils.discord_to_twitch_datetime(message.created_at)

    if user_info:
        user_id = user_info['id']
        avatar_url = user_info['profile_image_url']
        # 檢查該時間是否有實況
        vod_url, timestamp_seconds, vod_title = await utils.check_stream(
            user_id, target_time_utc) or (None, None, None)

        # 使用模組化的 embed 函數
        embed = utils.create_vod_embed(user_name, user_id, avatar_url,
                                       target_time_utc, vod_url,
                                       timestamp_seconds, vod_title)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message('not working', ephemeral=True)


# Get token
token = os.environ['DISCORD_BOT_TOKEN']


# Run main script
async def main():
    async with bot:
        await Load()
        await bot.start(token)


asyncio.run(main())

# Baby DD branch
