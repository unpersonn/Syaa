"""Moderation related commands."""

from __future__ import annotations

from datetime import timedelta

import discord
from discord.ext import commands

from utils.ui import SuccessEmbed, ErrorEmbed


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # purge messages
    @commands.hybrid_command(name="purge", description="Delete a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int) -> None:
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            # -1 to account for the command message itself
            actual_deleted = len(deleted) - 1
            embed = SuccessEmbed(f"Deleted **{actual_deleted if actual_deleted > 0 else 0}** messages.")
            await ctx.send(embed=embed, delete_after=5)
        except Exception as exc:
            await ctx.send(embed=ErrorEmbed(f"Failed to delete messages.\n`{exc}`"))

    # timeout user
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
            await ctx.send(embed=ErrorEmbed("You must mention a user to timeout!"))
            return

        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            embed = SuccessEmbed(f"Timed out **{member.mention}** for **{minutes}** minutes.")
            embed.Add_field(name="Reason", value=reason)
            embed.set_request_footer(ctx.author)
            await ctx.send(embed=embed)
        except Exception as exc:
            await ctx.send(embed=ErrorEmbed(f"Failed to timeout {member.name}.\n`{exc}`"))

    # kick user
    @commands.hybrid_command(name="kick", description="Kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx: commands.Context, member: discord.Member, reason: str = "None"
    ) -> None:
        if not member:
             await ctx.send(embed=ErrorEmbed("You must mention a user to kick!"))
             return

        try:
            await member.kick(reason=reason)
            embed = SuccessEmbed(f"Kicked **{member.display_name}**.")
            embed.add_field(name="Reason", value=reason)
            embed.set_request_footer(ctx.author)
            await ctx.send(embed=embed)
        except Exception as exc:
            await ctx.send(embed=ErrorEmbed(f"Failed to kick {member.name}.\n`{exc}`"))

    # ban member
    @commands.hybrid_command(name="ban", description="Ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx: commands.Context, member: discord.Member, reason: str = "None"
    ) -> None:
        if not member:
            await ctx.send(embed=ErrorEmbed("You must mention a user to ban!"))
            return

        try:
            await member.ban(reason=reason)
            embed = SuccessEmbed(f"Banned **{member.display_name}**.")
            embed.add_field(name="Reason", value=reason)
            embed.set_request_footer(ctx.author)
            await ctx.send(embed=embed)
        except Exception as exc:
            await ctx.send(embed=ErrorEmbed(f"Failed to ban {member.name}.\n`{exc}`"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))

