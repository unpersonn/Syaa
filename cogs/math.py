# cogs/math.py
import discord
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # perform calculation
    @commands.command(name="calc", help="Calculate mathematical expression.")
    async def calculate(self, ctx, *, expression: str):
        try:
            result = eval(expression)
            await ctx.send(f"the result of `{expression}` is `{result}`!")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Math(bot))