import discord
from discord.ext import commands
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

# TENOR API KEY
TENOR_API_KEY = os.getenv('TENOR_API')

class Actions(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def get_gif(self, search_term):

        # fetch random gif based on search term
        url = f'https://tenor.googleapis.com/v2/search?q={search_term}&key={TENOR_API_KEY}&limit=100'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
               # print(f"Tenor API Response: {data}") # debugging: print API response #
                if "results" in data and len(data["results"]) > 0:
                    selected_result = random.choice(data["results"])

                    # access different media formats
                    # you can choose any of the available formats; here we will use the 'gif' key
                    if "media_formats" in selected_result:
                        gif_url = selected_result["media_formats"].get("gif",{}).get("url")
                        if gif_url:
                            return gif_url
                        else:
                            print("No GIF URL found in media formats.")  # Debugging
                            return None
                    else:
                        print("No media formats found in the result.")  # Debugging
                        return None
                else:
                    print("No results found in Tenor API response.")  # Debugging
                    return None
            else:
                print(f"Failed to fetch GIF. Status code: {response.status_code}")  # Debugging
                return None

        except Exception as e:
            print(f"Error fetching GIF from Tenor: {str(e)}")
        
    # cuddle
    @commands.command(name="cuddle", help="Cuddles the mentioned user!")
    async def cuddle(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to cuddle!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("cute cuddle anime") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} cuddles {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "cuddle unperson too :>")
                else:
                    embed.set_footer(text = "keep cuddling unperson >_<")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No cuddles for you!")

    # hug
    @commands.command(name="hug", help="Hugs the mentioned user!")
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to hug!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("cute hug anime") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} hugs {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "hug unperson too :>")
                else:
                    embed.set_footer(text = "keep hugging unperson >_<")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No hugs for you!")

    # kiss
    @commands.command(name="kiss", help="Kisses the mentioned user!")
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to kiss!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("cute kiss anime") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} kisses {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "kiss unperson too :>")
                else:
                    embed.set_footer(text = "unperson loves kissies >_<")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No kissies for you!")

    # bonk
    @commands.command(name="bonk", help="Bonks the mentioned user!")
    async def bonk(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to bonk!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("bonk anime") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} bonks {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "bonk keto :>")
                else:
                    embed.set_footer(text = "don't bonk unperson u nub!")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No bonks for you!")

    # bully
    @commands.command(name="bully", help="Bullies the mentioned user!")
    async def bully(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to bonk!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("bullying anime") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} bullies {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "bully keto :>")
                else:
                    embed.set_footer(text = "oi don't bully unperson u nub!")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No bullying for you!")
                
    # shoot
    @commands.command(name="shoot", help="shoots the mentioned user!")
    async def shoot(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to kill!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("anime gun shoot") # fetch a random cuddle anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} shot {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "shoot keto :>")
                else:
                    embed.set_footer(text = "shooting unperson? how cute...")

                await ctx.send(embed=embed)
            else:
                await ctx.send("You don't even have a gun nub!")

    # pat
    @commands.command(name="pat", help="pats the mentioned user!")
    async def pat(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You need to mention someone to pat!")
            return # exit the command early to prevent further errors
        else:
            gif_url = self.get_gif("cute anime pats") # fetch a random paat anime gif
            if gif_url:
                embed = discord.Embed(
                    description = f"{ctx.author.name} shot {member.name}",
                    color = discord.Color.pink()
                )
                embed.set_image(url=gif_url)
                if member.id != 1025969591165403146:
                    embed.set_footer(text = "pat unperson :>")
                else:
                    embed.set_footer(text = "yay >_<")

                await ctx.send(embed=embed)
            else:
                await ctx.send("No pats for you!")



async def setup(bot):
    await bot.add_cog(Actions(bot))
