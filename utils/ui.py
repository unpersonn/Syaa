import datetime
from typing import Optional

import discord

# --- Colors ---
COLOR_MAIN = 0xFFA0C0  # Soft Pink
COLOR_SUCCESS = 0x57F287  # Discord Green
COLOR_ERROR = 0xED4245  # Discord Red
COLOR_WARNING = 0xFEE75C  # Discord Yellow


class SyaaEmbed(discord.Embed):
    """Base Embed for the bot with default styling."""

    def __init__(self, **kwargs):
        # Default color to Soft Pink if not specified
        if "color" not in kwargs:
            kwargs["color"] = COLOR_MAIN
        
        # Default timestamp to now if not specified
        if "timestamp" not in kwargs:
            kwargs["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

        super().__init__(**kwargs)

    def set_request_footer(self, user: discord.abc.User, text: str = ""):
        """Sets the footer with 'Requested by <user>'."""
        icon_url = user.display_avatar.url
        base_text = f"Requested by {user.display_name}"
        full_text = f"{base_text} • {text}" if text else base_text
        self.set_footer(text=full_text, icon_url=icon_url)


class SuccessEmbed(SyaaEmbed):
    """Embed for successful actions."""
    def __init__(self, description: str, **kwargs):
        super().__init__(description=f"✅ {description}", color=COLOR_SUCCESS, **kwargs)


class ErrorEmbed(SyaaEmbed):
    """Embed for failed actions or errors."""
    def __init__(self, description: str, **kwargs):
        super().__init__(description=f"❌ {description}", color=COLOR_ERROR, **kwargs)


class InfoEmbed(SyaaEmbed):
    """Embed for information."""
    def __init__(self, description: str, **kwargs):
        super().__init__(description=f"ℹ️ {description}", color=discord.Color.blue(), **kwargs)
