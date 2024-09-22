import asyncio
import os

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")


with open("token.txt") as file:
  token = file.read()


async def Load():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
  async with bot:
    await Load()
    await bot.start(token)


asyncio.run(main())
# # Retrieve token from the .env file
# load_dotenv()
# bot.run(os.getenv('TOKEN'))
