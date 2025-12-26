"""Fun commands cog."""

from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands

from utils.ui import SyaaEmbed, SuccessEmbed, ErrorEmbed, InfoEmbed
from .storage import get_leaderboard_async, get_user_stats_async, record_loss, record_win


class RPSView(discord.ui.View):
    def __init__(self, bot: commands.Bot, user: discord.Member, guild_id: int):
        super().__init__(timeout=60)
        self.bot = bot
        self.user = user
        self.guild_id = guild_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("Start your own game!", ephemeral=True)
            return False
        return True

    async def play(self, interaction: discord.Interaction, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        
        # Calculate result
        if choice == bot_choice:
            result = "It's a tie!"
            color = discord.Color.gold()
        elif (
            (choice == "rock" and bot_choice == "scissors")
            or (choice == "paper" and bot_choice == "rock")
            or (choice == "scissors" and bot_choice == "paper")
        ):
            result = "You win! 🎉"
            await record_win(self.guild_id, self.user.id)
            color = discord.Color.green()
        else:
            result = "You lose! 💀"
            await record_loss(self.guild_id, self.user.id)
            color = discord.Color.red()

        embed = SyaaEmbed(title="Rock Paper Scissors", color=color)
        embed.description = f"**{result}**"
        embed.add_field(name="Your Choice", value=choice.title(), inline=True)
        embed.add_field(name="My Choice", value=bot_choice.title(), inline=True)
        
        # Disable all buttons
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    @discord.ui.button(label="Rock", emoji="🪨", style=discord.ButtonStyle.secondary)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.play(interaction, "rock")

    @discord.ui.button(label="Paper", emoji="📄", style=discord.ButtonStyle.secondary)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.play(interaction, "paper")

    @discord.ui.button(label="Scissors", emoji="✂️", style=discord.ButtonStyle.secondary)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.play(interaction, "scissors")


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # coin flip
    @commands.hybrid_command(description="Flip a coin!")
    async def flip(self, ctx: commands.Context) -> None:
        embed = SyaaEmbed(title="Coin Flip")
        embed.description = "🪙 Flipping code..."
        message = await ctx.send(embed=embed)
        
        await asyncio.sleep(2)
        
        result = random.choice(["Heads", "Tails"])
        embed.description = f"The coin landed on **{result}**!"
        embed.set_thumbnail(url="https://media.tenor.com/B9O47r7_vK8AAAAi/coin-flip-coin.gif") # Generic Coin gif
        await message.edit(embed=embed)

    # rock, paper, scissors
    @commands.hybrid_command(description="Play rock, paper, scissors with the bot")
    async def rps(self, ctx: commands.Context) -> None:
        embed = SyaaEmbed(title="Rock Paper Scissors", description="Choose your weapon!")
        view = RPSView(self.bot, ctx.author, ctx.guild.id if ctx.guild else 0)
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(
        description="Show RPS stats for a user or this server's leaderboard"
    )
    async def rpsstats(
        self, ctx: commands.Context, member: discord.Member | None = None
    ) -> None:
        guild_id = ctx.guild.id if ctx.guild else 0

        if member is not None:
            wins, losses = await get_user_stats_async(guild_id, member.id)
            embed = SyaaEmbed(title=f"RPS Stats: {member.display_name}")
            embed.add_field(name="Wins", value=str(wins), inline=True)
            embed.add_field(name="Losses", value=str(losses), inline=True)
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
            return

        leaderboard = await get_leaderboard_async(guild_id)
        if not leaderboard:
            await ctx.send(embed=InfoEmbed("No RPS games have been played yet!"))
            return

        lines = []
        for index, (user_id, wins, losses) in enumerate(leaderboard, start=1):
            user = ctx.guild.get_member(user_id) if ctx.guild else self.bot.get_user(user_id)
            name = user.display_name if user else f"User {user_id}"
            lines.append(f"`{index}.` **{name}** • {wins}W / {losses}L")

        embed = SyaaEmbed(title="🏆 RPS Leaderboard")
        embed.description = "\n".join(lines)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
