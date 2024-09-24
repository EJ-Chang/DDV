import discord
from discord.ext import commands


class Test(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{__name__} is online!')

  @commands.command()
  # Get ping of the bot
  async def ping(self, ctx):
    ping_embed = discord.Embed(title="Ping",
                               description="Latency in ms",
                               color=discord.Color.random())
    ping_embed.add_field(name=f"{self.bot.user.display_name}'s latency (ms)",
                         value=f"{round(self.bot.latency * 1000)}ms.",
                         inline=False)
    ping_embed.set_footer(text=f"請求由 {ctx.author.display_name} 發送",
                          icon_url=ctx.author.avatar)
    await ctx.send(embed=ping_embed)

  # Greeting
  @commands.command()
  async def greet(self, ctx):
    response = 'Hello, I am your discord bot'
    await ctx.send(response)

  @commands.command()
  async def list_command(self, ctx):
    response = 'You can use the following commands: \n !greet \n !list_command \n !functions'
    await ctx.send(response)

  @commands.command()
  async def functions(self, ctx):
    response = 'I am a simple Discord chatbot! I will reply to your command!'
    await ctx.send(response)

  # 自己寫一個!command, 有化名的版本
  @commands.command(aliases=['hi', 'ayo'])
  async def yobro(self, ctx):
    await ctx.send(f'Ayo Bro! Noice do meet ja!, {ctx.author.mention}!')

  # embeded message
  @commands.command()
  async def sendembed(self, ctx):
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


async def setup(bot):
  await bot.add_cog(Test(bot))
