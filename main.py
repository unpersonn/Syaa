"""Main entry point for the bot.

This file defines a subclass of :class:`commands.Bot` which loads all
extensions on start and ensures both prefix and slash commands are
available.  All cogs are loaded during ``setup_hook`` so they are ready
before the bot connects to Discord.
"""

from __future__ import annotations

import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------------------------------------------------------------------------
# Prefix handling
# ---------------------------------------------------------------------------

DB_PATH = "guild_prefixes.db"
DEFAULT_PREFIX = "!"

# Ensure the database and table exist
with sqlite3.connect(DB_PATH) as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS guild_prefixes (
            guild_id INTEGER PRIMARY KEY,
            prefix   TEXT NOT NULL
        )
        """
    )


def _get_guild_prefix(guild_id: int | None) -> str:
    """Return the stored prefix for ``guild_id`` or ``DEFAULT_PREFIX``."""

    if guild_id is None:
        return DEFAULT_PREFIX

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT prefix FROM guild_prefixes WHERE guild_id = ?", (guild_id,)
        )
        row = cur.fetchone()

    return row[0] if row else DEFAULT_PREFIX


def get_prefix(bot: commands.Bot, message: discord.Message) -> list[str]:
    """Return the prefix list for the current guild."""

    prefix = _get_guild_prefix(message.guild.id if message.guild else None)
    return commands.when_mentioned_or(prefix)(bot, message)


class SyaaBot(commands.Bot):
    """Bot subclass that handles cog loading and command syncing."""

    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=get_prefix, intents=intents)

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

    current = _get_guild_prefix(interaction.guild_id)
    await interaction.response.send_message(
        f"The current bot prefix is: {current}"
    )


@bot.tree.command(description="Set the bot prefix for this guild")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(prefix="The new prefix to use")
async def setprefix(interaction: discord.Interaction, prefix: str) -> None:
    """Slash command to store a new guild prefix."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "REPLACE INTO guild_prefixes (guild_id, prefix) VALUES (?, ?)",
            (interaction.guild_id, prefix),
        )
        conn.commit()

    await interaction.response.send_message(f"Prefix set to: {prefix}")


@bot.tree.command(description="Reset the bot prefix for this guild")
@app_commands.checks.has_permissions(administrator=True)
async def resetprefix(interaction: discord.Interaction) -> None:
    """Remove any custom prefix for this guild."""

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM guild_prefixes WHERE guild_id = ?",
            (interaction.guild_id,),
        )
        conn.commit()

    await interaction.response.send_message(
        f"Prefix reset to: {DEFAULT_PREFIX}"
    )


bot.run(TOKEN)

