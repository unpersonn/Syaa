"""Fun commands cog."""

from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands

from .storage import get_leaderboard, get_user_stats, record_loss, record_win


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

        guild_id = ctx.guild.id if ctx.guild else 0

        if user_choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (
            (user_choice.lower() == "rock" and bot_choice == "scissors")
            or (user_choice.lower() == "paper" and bot_choice == "rock")
            or (user_choice.lower() == "scissors" and bot_choice == "paper")
        ):
            result = "You win!"
            record_win(guild_id, ctx.author.id)
        else:
            result = "You lose!"
            record_loss(guild_id, ctx.author.id)

        await ctx.send(
            f"You chose {user_choice}, I chose {bot_choice}, {result}.",
        )

    @commands.hybrid_command(
        description="Show RPS stats for a user or this server's leaderboard"
    )
    async def rpsstats(
        self, ctx: commands.Context, member: discord.Member | None = None
    ) -> None:
        guild_id = ctx.guild.id if ctx.guild else 0

        if member is not None:
            wins, losses = get_user_stats(guild_id, member.id)
            await ctx.send(
                f"{member.display_name} has {wins} wins and {losses} losses in RPS."
            )
            return

        leaderboard = get_leaderboard(guild_id)
        if not leaderboard:
            await ctx.send("No RPS games have been played yet!")
            return

        lines = []
        for index, (user_id, wins, losses) in enumerate(leaderboard, start=1):
            user = ctx.guild.get_member(user_id) if ctx.guild else self.bot.get_user(user_id)
            name = user.display_name if user else f"User {user_id}"
            lines.append(f"{index}. {name} - {wins}W/{losses}L")

        await ctx.send("RPS Leaderboard:\n" + "\n".join(lines))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
