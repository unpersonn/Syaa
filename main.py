"""Main entry point for the bot.

This file defines a subclass of :class:`commands.Bot` which loads all
extensions on start and ensures both prefix and slash commands are
available.  All cogs are loaded during ``setup_hook`` so they are ready
before the bot connects to Discord.
"""

from __future__ import annotations

import logging
import os
import traceback

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_PREFIX = "!"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


class SyaaBot(commands.Bot):
    """Bot subclass that handles cog loading and command syncing."""

    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        """Load extensions and sync the application command tree."""

        # Initialize Database
        from database.db import init_db
        await init_db()

        # Load available extensions
        for extension in [
            "cogs.math",
            "cogs.fun",
            "cogs.moderation",
            "cogs.actions",
            "cogs.hangman",
            "cogs.tictactoe",
            "cogs.help",
        ]:
            try:
                await self.load_extension(extension)
            except Exception:  # pragma: no cover - log for debugging
                logger.exception("Failed to load %s", extension)

        # Sync slash commands
        await self.tree.sync()

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handle errors arising from command invocation."""
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command.")
            return

        logger.error(
            "Unhandled exception in command '%s'",
            getattr(ctx.command, "name", "unknown"),
            exc_info=error,
        )
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        await ctx.send(f"```py\n{tb}\n```")

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        """Handle errors raised by slash or hybrid commands.

        This mirrors :meth:`on_command_error` so that interactions that fail
        don't simply time out with "application did not respond".  The error
        is logged and the traceback is sent back to the user.
        """

        if isinstance(error, app_commands.CommandNotFound):
            if interaction.response.is_done():
                await interaction.followup.send(
                    "Unknown command.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Unknown command.", ephemeral=True
                )
            return

        logger.error(
            "Unhandled exception in app command '%s'",
            interaction.command.name if interaction.command else "unknown",
            exc_info=error,
        )
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        if interaction.response.is_done():
            await interaction.followup.send(f"```py\n{tb}\n```", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"```py\n{tb}\n```", ephemeral=True
            )


bot = SyaaBot()


@bot.event
async def on_ready() -> None:
    """Announce successful login and set presence."""

    logger.info("%s has logged in!", bot.user)

    activity = discord.Game(name="with Unperson!")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.tree.command(description="Show the current bot prefix")
async def prefix(interaction: discord.Interaction) -> None:
    """Slash command to display the configured prefix."""

    await interaction.response.send_message(
        f"The current bot prefix is: {DEFAULT_PREFIX}"
    )


bot.run(TOKEN)

