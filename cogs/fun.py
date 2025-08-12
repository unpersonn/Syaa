"""Fun commands cog."""

from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # coin flip
    @commands.hybrid_command(description="Flip a coin!")
    async def flip(self, ctx: commands.Context) -> None:
        message = await ctx.send("Flipping a coin...")
        await asyncio.sleep(3)
        result = random.choice(["Heads", "Tails"])
        await message.edit(content=f"{result}!")

    # rock, paper, scissors
    @commands.hybrid_command(description="Play rock, paper, scissors with the bot")
    async def rps(self, ctx: commands.Context, user_choice: str) -> None:
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        if user_choice.lower() not in choices:
            await ctx.send("Please choose rock, paper, or scissors!")
            return

        if user_choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (
            (user_choice.lower() == "rock" and bot_choice == "scissors")
            or (user_choice.lower() == "paper" and bot_choice == "rock")
            or (user_choice.lower() == "scissors" and bot_choice == "paper")
        ):
            result = "You win!"
        else:
            result = "You lose!"

        await ctx.send(
            f"You chose {user_choice}, I chose {bot_choice}, {result}."
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))

