import asyncio
import os
from pickle import TRUE

import discord
from discord.ext import commands

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
    print(f"Logged in as {bot.user.name}")

    # 設定狀態為「聽音樂」
    # 目前好像只有聽(音樂) 玩(遊戲) 跟觀賞什麼可以選
    activity = discord.Activity(type=discord.ActivityType.listening,
                                name="煌Sir有汐") 
                                # TODO:想要 random or 跑馬燈
    await bot.change_presence(status=discord.Status.online, activity=activity)

# ADD context menu
@bot.tree.context_menu(name="Show join date")
async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'Member joined at: {member.joined_at}', ephemeral=True)


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
