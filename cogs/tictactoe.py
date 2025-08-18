"""TicTacToe game cog."""

from __future__ import annotations

import discord
from discord.ext import commands

from .storage import (
    record_tictactoe_win,
    record_tictactoe_loss,
    get_tictactoe_user_stats,
    get_tictactoe_leaderboard,
)


class TicTacToeButton(discord.ui.Button):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(style=discord.ButtonStyle.secondary, label=" ", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction) -> None:  # type: ignore[override]
        view: TicTacToeView = self.view  # type: ignore[assignment]
        await view.handle_move(interaction, self)


class TicTacToeView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member) -> None:
        super().__init__(timeout=180)
        self.players = (player1, player2)
        self.current = 0
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    async def handle_move(
        self, interaction: discord.Interaction, button: TicTacToeButton
    ) -> None:
        if interaction.user not in self.players:
            await interaction.response.send_message(
                "You're not playing this game.", ephemeral=True
            )
            return

        if interaction.user != self.players[self.current]:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        if self.board[button.y][button.x]:
            await interaction.response.send_message(
                "That spot is already taken.", ephemeral=True
            )
            return

        mark = "X" if self.current == 0 else "O"
        button.label = mark
        button.style = (
            discord.ButtonStyle.danger if self.current == 0 else discord.ButtonStyle.success
        )
        button.disabled = True
        self.board[button.y][button.x] = mark

        winner = self.check_winner()
        embed = discord.Embed(title="Tic Tac Toe")
        guild_id = interaction.guild.id if interaction.guild else 0

        if winner is not None:
            for child in self.children:
                child.disabled = True
            winner_member = self.players[winner]
            loser_member = self.players[winner ^ 1]
            embed.description = f"{winner_member.mention} wins!"
            await record_tictactoe_win(guild_id, winner_member.id)
            await record_tictactoe_loss(guild_id, loser_member.id)
            self.stop()
        elif self.is_draw():
            for child in self.children:
                child.disabled = True
            embed.description = "It's a draw!"
            self.stop()
        else:
            self.current ^= 1
            embed.description = f"It's {self.players[self.current].mention}'s turn."

        await interaction.response.edit_message(embed=embed, view=self)

    def check_winner(self) -> int | None:
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[y][x] for y in range(3)] for x in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] and line.count(line[0]) == 3:
                return 0 if line[0] == "X" else 1
        return None

    def is_draw(self) -> bool:
        return all(cell for row in self.board for cell in row)


class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Challenge another user to Tic Tac Toe")
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member) -> None:
        if opponent == ctx.author or opponent.bot:
            await ctx.send("Please challenge someone else!")
            return

        view = TicTacToeView(ctx.author, opponent)
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=(
                f"{ctx.author.mention} vs {opponent.mention}\n"
                f"{ctx.author.mention} goes first."
            ),
        )
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(
        description="Show Tic Tac Toe stats for a user or this server's leaderboard"
    )
    async def tictactoestats(
        self, ctx: commands.Context, member: discord.Member | None = None
    ) -> None:
        guild_id = ctx.guild.id if ctx.guild else 0

        if member is not None:
            wins, losses = await get_tictactoe_user_stats(guild_id, member.id)
            await ctx.send(
                f"{member.display_name} has {wins} wins and {losses} losses in Tic Tac Toe."
            )
            return

        leaderboard = await get_tictactoe_leaderboard(guild_id)
        if not leaderboard:
            await ctx.send("No Tic Tac Toe games have been played yet!")
            return

        lines = []
        for index, (user_id, wins, losses) in enumerate(leaderboard, start=1):
            user = ctx.guild.get_member(user_id) if ctx.guild else self.bot.get_user(user_id)
            name = user.display_name if user else f"User {user_id}"
            lines.append(f"{index}. {name} - {wins}W/{losses}L")

        await ctx.send("Tic Tac Toe Leaderboard:\n" + "\n".join(lines))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicTacToe(bot))
