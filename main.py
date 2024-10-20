import asyncio
import os
from pickle import TRUE
import requests
import discord
from discord.ext import commands
from datetime import datetime, timedelta

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


# ADD context menu: Join
@bot.tree.context_menu(name="Show join date")
async def get_joined_date(interaction: discord.Interaction,
                          member: discord.Member):
    if member.joined_at:
        await interaction.response.send_message(
            f'Member joined at: {discord.utils.format_dt(member.joined_at)}')
    else:
        await interaction.response.send_message('Join date unknown.')


# ADD context menu: MSG
@bot.tree.context_menu(name="Show msg create date")
async def get_message_create_date(interaction: discord.Interaction,
                                  message: discord.Message):
    if message.created_at:
        await interaction.response.send_message(
            f'This msg was created at: {discord.utils.format_dt(message.created_at)}'
        )
    else:
        await interaction.response.send_message('MSG date unknown.')

# Here's twitch info functions I need
# Get info from Twitch
async def username_2_user_info(user_name):
    url = f'https://api.twitch.tv/helix/users?login={user_name}'
    headers = {
                'Client-ID': TWITCH_CLIENT_ID,
                'Authorization': f'Bearer {TWITCH_TOKEN}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['data'][0]  # 返回用戶資料
    else:
        print(f"Error fetching user info: {response.status_code}")
        return None

# Get all past streams (VODs)
async def get_all_past_streams(user_id):
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
async def check_stream(user_name, target_time_utc):
    user_info =  await username_2_user_info(user_name)
    if user_info:
        user_id = user_info['id']
        vods = await get_all_past_streams(user_id)

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
# async def organize_embed_twitch_msg()



# Context menu: MSG time to VOD feedback
@bot.tree.context_menu(name="SEKI's VOD time travel")
async def get_msg_for_timetravel_at_seki(interaction: discord.Interaction,
                                         message: discord.Message):

    user_name = 'seki_meridian'
    user_info = await username_2_user_info(user_name)
    target_time_utc = message.created_at
    if user_info:
        user_id = user_info['id']
        avatar_url = user_info['profile_image_url']
        # 檢查該時間是否有實況
        vod_url, timestamp_seconds, vod_title = await check_stream(
                user_id, target_time_utc)

        embed = discord.Embed(title=f"{user_name}'s Info")
        embed.set_thumbnail(url=avatar_url)

        embed = discord.Embed(title=f"{user_name}'s Info")
        embed.add_field(name='UserID is:', value=f'{user_id}')
        embed.add_field(name='查詢的時間是:', value=f'{target_time_utc}')
        embed.add_field(name='URL', value= vod_url)
        embed.set_thumbnail(url=avatar_url)
        
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message('not working')


# Get token
token = os.environ['DISCORD_BOT_TOKEN']


# Run main script
async def main():
    async with bot:
        await Load()
        await bot.start(token)


asyncio.run(main())

# Baby DD branch
