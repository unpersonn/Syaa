"""Hangman game cog."""

from __future__ import annotations

import random
import string

import discord
from discord.ext import commands

from .storage import record_hangman_win, record_hangman_loss

WORDS = [
    "python",
    "discord",
    "hangman",
    "bot",
    "cog",
    "extension",
    "asyncio",
    "database",
]


class HangmanButton(discord.ui.Button):
    def __init__(self, letter: str) -> None:
        index = string.ascii_lowercase.index(letter)
        super().__init__(
            label=letter.upper(),
            style=discord.ButtonStyle.secondary,
            row=index // 5,
        )
        self.letter = letter

    async def callback(self, interaction: discord.Interaction) -> None:  # type: ignore[override]
        view: HangmanView = self.view  # type: ignore[assignment]
        await view.handle_guess(interaction, self)


class HangmanView(discord.ui.View):
    def __init__(self, players: list[discord.Member], word: str) -> None:
        super().__init__(timeout=180)
        self.players = players
        self.word = word
        self.progress = ["_" if c.isalpha() else c for c in word]
        self.misses = 0
        self.max_misses = 6

        for letter in string.ascii_lowercase:
            self.add_item(HangmanButton(letter))

    def format_status(self) -> str:
        return (
            f"Word: {' '.join(self.progress)}\n"
            f"Misses: {self.misses}/{self.max_misses}"
        )

    async def handle_guess(self, interaction: discord.Interaction, button: HangmanButton) -> None:
        if interaction.user not in self.players:
            await interaction.response.send_message(
                "You're not playing this game.", ephemeral=True
            )
            return

        button.disabled = True
        letter = button.letter
        finished: str | None = None

        if letter in self.word:
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.progress[idx] = char
            if "_" not in self.progress:
                finished = "win"
        else:
            self.misses += 1
            button.style = discord.ButtonStyle.danger
            if self.misses >= self.max_misses:
                finished = "loss"

        guild_id = interaction.guild.id if interaction.guild else 0

        if finished == "win":
            for child in self.children:
                child.disabled = True
            for player in self.players:
                await record_hangman_win(guild_id, player.id)
            description = (
                f"{' and '.join(p.mention for p in self.players)} guessed the word "
                f"**{self.word}**!"
            )
            embed = discord.Embed(title="Hangman", description=description)
            await interaction.response.edit_message(embed=embed, view=self)
            self.stop()
            return

        if finished == "loss":
            for child in self.children:
                child.disabled = True
            for player in self.players:
                await record_hangman_loss(guild_id, player.id)
            description = f"No more guesses! The word was **{self.word}**."
            embed = discord.Embed(title="Hangman", description=description)
            await interaction.response.edit_message(embed=embed, view=self)
            self.stop()
            return

        embed = discord.Embed(title="Hangman", description=self.format_status())
        await interaction.response.edit_message(embed=embed, view=self)


class Hangman(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Play a game of Hangman")
    async def hangman(self, ctx: commands.Context, opponent: discord.Member | None = None) -> None:
        players = [ctx.author]
        if opponent is not None:
            if opponent == ctx.author or opponent.bot:
                await ctx.send("Please challenge someone else!")
                return
            players.append(opponent)

        word = random.choice(WORDS)
        view = HangmanView(players, word)
        embed = discord.Embed(
            title="Hangman",
            description=(
                f"Players: {' and '.join(p.mention for p in players)}\n" + view.format_status()
            ),
        )
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hangman(bot))
