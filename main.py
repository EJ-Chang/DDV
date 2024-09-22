# Import the required modules
import os
import asyncio
import discord
from discord import embeds
from discord.ext import commands
from dotenv import load_dotenv
from discord.ui import Select, View
from twitchio.ext import commands as twitch_commands
import requests

# Twitch API here
TWITCH_CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
TWITCH_TOKEN = '9fjv0bwl9kpf39zjww6qlnfydvpumm'

# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


# Get info from twtich
def get_twitch_user_info(user_name):
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


def get_twitch_schedule(user_id):
    url = f'https://api.twitch.tv/helix/schedule?broadcaster_id={user_id}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['data']  # 返回排程資料
    else:
        print(f"Error fetching schedule: {response.status_code}")
        return None


@bot.command(name="viewCarry")
async def view_carry(ctx):
    user_name = "carrymaybe484"  # Twitch ID
    user_info = get_twitch_user_info(user_name)

    if user_info:
        user_id = user_info['id']
        avatar_url = user_info['profile_image_url']

        # 獲取排程資訊
        schedule_info = get_twitch_schedule(user_id)

        embed = discord.Embed(title=f"{user_name}'s Info")
        embed.set_image(url=avatar_url)

        if schedule_info:
            # 格式化排程資訊
            schedule_text = "\n".join(f"{item['start_time']} - {item['title']}"
                                      for item in schedule_info)
            embed.add_field(name="Upcoming Schedule",
                            value=schedule_text or "No upcoming streams.")
        else:
            embed.add_field(name="Upcoming Schedule",
                            value="Could not retrieve schedule.")

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Could not retrieve info for {user_name}.")


# -----eee---www---
# Set the confirmation message when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


# Set the commands for your bot
@bot.command()
async def greet(ctx):
    response = 'Hello, I am your discord bot'
    await ctx.send(response)


@bot.command()
async def list_command(ctx):
    response = 'You can use the following commands: \n !greet \n !list_command \n !functions'
    await ctx.send(response)


@bot.command()
async def functions(ctx):
    response = 'I am a simple Discord chatbot! I will reply to your command!'
    await ctx.send(response)


# 自己寫一個!command, 有化名的版本
@bot.command(aliases=['hi', 'ayo'])
async def yobro(ctx):
    await ctx.send(f'Ayo Bro! Noice do meet ja!, {ctx.author.mention}!')


# embeded message
@bot.command()
async def sendembed(ctx):
    embeded_msg = discord.Embed(title="This is an embed message",
                                description="This is a description",
                                color=discord.Color.random())
    embeded_msg.set_thumbnail(url=ctx.author.avatar.url)
    embeded_msg.add_field(name="Field 1",
                          value="Value of field 1",
                          inline=False)
    embeded_msg.set_image(url=ctx.guild.icon.url)
    embeded_msg.set_author(name=f"{ctx.author.name}")
    await ctx.send(embed=embeded_msg)


# Get ping of the bot
@bot.command()
async def ping(ctx):
    ping_embed = discord.Embed(title="Ping",
                               description="Latency in ms",
                               color=discord.Color.random())
    ping_embed.add_field(name=f"{bot.user.display_name}'s latency (ms)",
                         value=f"{round(bot.latency * 1000)}ms.",
                         inline=False)
    ping_embed.set_footer(text=f"請求由 {ctx.author.display_name} 發送",
                          icon_url=ctx.author.avatar)
    await ctx.send(embed=ping_embed)


# Retrieve token from the .env file
load_dotenv()
bot.run(os.getenv('TOKEN'))
