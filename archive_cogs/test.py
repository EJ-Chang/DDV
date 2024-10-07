import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import DISCORD_EPOCH


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} is online!')

    @app_commands.command(name="ping", description="Check the ping of my bot.")
    # Get ping of the bot
    async def ping(self, interaction: discord.Interaction):
        ping_embed = discord.Embed(title="Ping",
                                                             description="Latency in ms",
                                                             color=discord.Color.random())
        ping_embed.add_field(name=f"{self.bot.user.display_name}'s latency (ms)",
                                                 value=f"{round(self.bot.latency * 1000)}ms.",
                                                 inline=False)
        ping_embed.set_footer(text=f"請求由 {interaction.user.display_name} 發送",
                                                    icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=ping_embed)

    # Greeting
    @app_commands.command(name='greet', description='Greet the user.')
    async def greet(self, interaction: discord.Interaction):
        response = 'Hello, I am your discord bot'
        await interaction.response.send_message(response)

    @app_commands.command()
    async def list_command(self, interaction: discord.Interaction):
        response = "You can use the following commands: \n !greet \n !list_command \n !functions"
        await interaction.response.send_message(response)

    @app_commands.command()
    async def functions(self, interaction: discord.Interaction):
        response = 'I am a simple Discord chatbot! I will reply to your command!'
        await interaction.response.send_message(response)

    # 自己寫一個 slash command, 有化名的版本
    @app_commands.command(name='hi')  # 可能不支援
    async def yobro(self, interaction: discord.Interaction):
        await interaction.response.send_message(
                f'Ayo Bro! Noice do meet ja!, {interaction.user.mention}!')

    # embeded message
    @app_commands.command()
    async def sendembed(self, interaction: discord.Interaction):
        embeded_msg = discord.Embed(title="This is an embed message",
                                                                description="This is a description",
                                                                color=discord.Color.random())
        embeded_msg.set_thumbnail(url=interaction.user.avatar.url)
        embeded_msg.add_field(name="Field 1",
                                                    value="Value of field 1",
                                                    inline=False)
        embeded_msg.set_image(url=interaction.guild.icon.url)
        embeded_msg.set_author(name=f"{interaction.user.name}")
        await interaction.response.send_message(embed=embeded_msg)


async def setup(bot):
    await bot.add_cog(Test(bot))
