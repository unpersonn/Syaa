# cogs/moderation.py
import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # purge messages
    @commands.command(name="purge", help="Deletes a specified number of messages.")
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted {amount} messages.", delete_after = 5)

        except Exception as e:
            await ctx.send(f"Failed to delete messages. Error: {str(e)}")

    # timeout user (simple version)
    @commands.command(name="timeout", help="Timeout a user for a specified duration (in minutes)")
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, reason: str = "None"):
        if not member:
            await ctx.send("You must mention a user to timeout!")

        else:
            try:
                duration = timedelta(minutes=minutes)
                await member.timeout(duration)
                await ctx.send(f"{member.name} has been timed out for {minutes} minute(s). Reason: {reason}!")
            except Exception as e:
                await ctx.send(f"Failed to timeout {member.name}. Error: {str(e)}")

    # kick user
    @commands.command(name="kick", help="Kick a user from the server.")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, reason: str = "None"):
        if not member:
            await ctx.send("You must mention a user to kick!")
        else:
            try:
                await member.kick(reason=reason)
                await ctx.send(f"{member.name} has been kicked!")
            except Exception as e:
                await ctx.send(f"Failed to kick {member.name}. Reason: {str(e)}")
    
    # ban member
    @commands.command(name="ban", help="Ban a user from the server")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, reason: str = "None"):
        if not member:
            await ctx.send("You must mention a user to kick!")
        else:
            try:
                await member.ban(reason=reason)
                await ctx.send(f"{member.name} has been banned!")
            except Exception as e:
                await ctx.send(f"Failed to ban {member.name}. Reason: {str(e)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))