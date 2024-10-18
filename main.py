import discord
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has logged in!")
    
    # load cogs
    try:
        await bot.load_extension("cogs.math")
        await bot.load_extension("cogs.fun")
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.actions")
        print("cog(s) has loaded successfully")

    except Exception as e:
        print(f"failed to load cog(s): {str(e)}")

    # rich presence
    activity = discord.Game(name="with Unperson!")
    '''discord.Activity(type=discord.ActivityType.listening, name="music")
    discord.Activity(type=discord.ActivityType.watching, name="anime")'''
    await bot.change_presence(status=discord.Status.online, activity=activity)

    # sync slash commands
    await bot.tree.sync()

    
@bot.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.client.ws.latency}")
bot.run(TOKEN)