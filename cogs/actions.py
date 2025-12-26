"""Action commands such as cuddle, hug, and more.

All commands are implemented as hybrid commands so they can be invoked
either via prefix or as slash commands.  A shared helper handles the
repeated work of fetching GIFs and composing the embeds.
"""

from __future__ import annotations

import os
import random
from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TENOR_API_KEY = os.getenv("TENOR_API")


class Actions(commands.Cog):
    """Cog providing various interaction commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def get_gif(self, search_term: str) -> Optional[str]:
        """Fetch a random GIF URL from Tenor for ``search_term``."""

        url = (
            "https://tenor.googleapis.com/v2/search"
            f"?q={search_term}&key={TENOR_API_KEY}&limit=100"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
        results = data.get("results", [])
        if not results:
            return None
        choice = random.choice(results)
        media = choice.get("media_formats", {})
        return media.get("gif", {}).get("url")

    async def _action(
        self,
        ctx: commands.Context,
        member: Optional[discord.Member],
        verb: str,
        sentence: str,
        search_term: str,
        footer_other: str,
        footer_self: str,
        failure: str,
    ) -> None:
        """Generic helper used by the action commands."""

        if member is None:
            await ctx.send(embed=discord.Embed(description=f"You need to mention someone to {verb}!", color=discord.Color.red()))
            return

        gif_url = await self.get_gif(search_term)
        if gif_url is None:
            await ctx.send(embed=discord.Embed(description=failure, color=discord.Color.red()))
            return

        from utils.ui import SyaaEmbed # Local import to avoid circular dependency issues if any
        
        embed = SyaaEmbed(
            description=f"**{ctx.author.name}** {sentence} **{member.name}**!",
        )
        embed.set_image(url=gif_url)
        embed.set_footer(
            text=footer_other if member.id != 1025969591165403146 else footer_self
        )
        await ctx.send(embed=embed)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    @commands.hybrid_command(description="Cuddle the mentioned user!")
    async def cuddle(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "cuddle",
            "cuddles",
            "cute cuddle anime",
            "cuddle unperson too :>",
            "keep cuddling unperson >_<",
            "No cuddles for you!",
        )

    @commands.hybrid_command(description="Hug the mentioned user!")
    async def hug(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "hug",
            "hugs",
            "cute hug anime",
            "hug unperson too :>",
            "keep hugging unperson >_<",
            "No hugs for you!",
        )

    @commands.hybrid_command(description="Kiss the mentioned user!")
    async def kiss(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "kiss",
            "kisses",
            "cute kiss anime",
            "kiss unperson too :>",
            "unperson loves kissies >_<",
            "No kissies for you!",
        )

    @commands.hybrid_command(description="Bonk the mentioned user!")
    async def bonk(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "bonk",
            "bonks",
            "bonk anime",
            "bonk keto :>",
            "don't bonk unperson u nub!",
            "No bonks for you!",
        )

    @commands.hybrid_command(description="Bully the mentioned user!")
    async def bully(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "bully",
            "bullies",
            "bullying anime",
            "bully keto :>",
            "oi don't bully unperson u nub!",
            "No bullying for you!",
        )

    @commands.hybrid_command(description="Shoot the mentioned user!")
    async def shoot(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "shoot",
            "shot",
            "anime gun shoot",
            "shoot keto :>",
            "shooting unperson? how cute...",
            "You don't even have a gun nub!",
        )

    @commands.hybrid_command(description="Pat the mentioned user!")
    async def pat(
        self, ctx: commands.Context, member: Optional[discord.Member] = None
    ) -> None:
        await self._action(
            ctx,
            member,
            "pat",
            "pats",
            "cute anime pats",
            "pat unperson :>",
            "yay >_<",
            "No pats for you!",
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Actions(bot))

