"""Moderation related commands."""

from __future__ import annotations

from datetime import timedelta

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # purge messages
    @commands.hybrid_command(name="purge", description="Delete a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int) -> None:
        try:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted {amount} messages.", delete_after=5)
        except Exception as exc:
            await ctx.send(f"Failed to delete messages. Error: {exc}")

    # timeout user (simple version)
    @commands.hybrid_command(
        name="timeout",
        description="Timeout a user for a specified duration (in minutes)",
    )
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        minutes: int,
        reason: str = "None",
    ) -> None:
        if not member:
            await ctx.send("You must mention a user to timeout!")
            return

        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            await ctx.send(
                f"{member.name} has been timed out for {minutes} minute(s). Reason: {reason}!"
            )
        except Exception as exc:
            await ctx.send(f"Failed to timeout {member.name}. Error: {exc}")

    # kick user
    @commands.hybrid_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx: commands.Context, member: discord.Member, reason: str = "None"
    ) -> None:
        if not member:
            await ctx.send("You must mention a user to kick!")
            return

        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.name} has been kicked!")
        except Exception as exc:
            await ctx.send(f"Failed to kick {member.name}. Reason: {exc}")

    # ban member
    @commands.hybrid_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx: commands.Context, member: discord.Member, reason: str = "None"
    ) -> None:
        if not member:
            await ctx.send("You must mention a user to kick!")
            return

        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned!")
        except Exception as exc:
            await ctx.send(f"Failed to ban {member.name}. Reason: {exc}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))

