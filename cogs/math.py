"""Mathematics related commands."""

from __future__ import annotations

import discord
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # perform calculation
    @commands.hybrid_command(name="calc", description="Calculate a mathematical expression")
    async def calculate(self, ctx: commands.Context, *, expression: str) -> None:
        try:
            result = eval(expression)
            await ctx.send(f"The result of `{expression}` is `{result}`!")
        except Exception as exc:
            await ctx.send(f"Error: {exc}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Math(bot))

