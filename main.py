"""Main entry point for the bot.

This file defines a subclass of :class:`commands.Bot` which loads all
extensions on start and ensures both prefix and slash commands are
available.  All cogs are loaded during ``setup_hook`` so they are ready
before the bot connects to Discord.
"""

from __future__ import annotations

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_PREFIX = "!"


class SyaaBot(commands.Bot):
    """Bot subclass that handles cog loading and command syncing."""

    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),
            intents=intents,
        )

    async def setup_hook(self) -> None:
        """Load extensions and sync the application command tree."""

        # Load available extensions
        for extension in [
            "cogs.math",
            "cogs.fun",
            "cogs.moderation",
            "cogs.actions",
        ]:
            try:
                await self.load_extension(extension)
            except Exception as exc:  # pragma: no cover - log for debugging
                print(f"Failed to load {extension}: {exc}")

        # Sync slash commands
        await self.tree.sync()


bot = SyaaBot()


@bot.event
async def on_ready() -> None:
    """Announce successful login and set presence."""

    print(f"{bot.user} has logged in!")

    activity = discord.Game(name="with Unperson!")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.tree.command(description="Show the current bot prefix")
async def prefix(interaction: discord.Interaction) -> None:
    """Slash command to display the configured prefix."""

    await interaction.response.send_message(
        f"The current bot prefix is: {DEFAULT_PREFIX}"
    )


bot.run(TOKEN)

