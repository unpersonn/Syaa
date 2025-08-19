"""Tic-tac-toe game cog."""

from __future__ import annotations

import asyncio
import random

import discord
from discord.ext import commands


class TicTacToeView(discord.ui.View):
    """Tic-tac-toe game view.

    This view manages the game state and interactions for a single game of
    tic-tac-toe.
    """

    def __init__(
        self, bot: commands.Bot, player1: discord.Member, player2: discord.Member
    ):
        super().__init__(timeout=180.0)
        self.bot = bot
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = [0] * 9  # 0: empty, 1: player1, 2: player2

        # Add buttons to the view
        for i in range(9):
            self.add_item(
                TicTacToeButton(style=discord.ButtonStyle.secondary, row=i // 3, custom_id=str(i))
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if the interaction user is the current player."""
        if interaction.user == self.current_player:
            return True
        await interaction.response.send_message(
            "It's not your turn!", ephemeral=True
        )
        return False

    async def on_timeout(self) -> None:
        """Handle view timeout."""
        for item in self.children:
            item.disabled = True
        # It's possible the message was already edited by the game ending
        if self.message:
            await self.message.edit(content="Game timed out.", view=self)

    async def handle_turn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """Handle a player's turn, including the bot's turn if applicable."""
        position = int(button.custom_id)
        player_value = 1 if self.current_player == self.player1 else 2
        player_symbol = "X" if player_value == 1 else "O"
        button_style = (
            discord.ButtonStyle.primary
            if player_value == 1
            else discord.ButtonStyle.danger
        )

        self.board[position] = player_value
        button.label = player_symbol
        button.style = button_style
        button.disabled = True

        if self.check_win(player_value):
            await self.end_game(interaction, f"{self.current_player.mention} wins!")
            return

        if 0 not in self.board:
            await self.end_game(interaction, "It's a draw!")
            return

        # Switch player
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )
        await interaction.response.edit_message(
            content=f"It's {self.current_player.mention}'s turn.", view=self
        )

        # If the new player is the bot, trigger its move
        if self.current_player == self.bot.user:
            await self.bot_move()

    def check_win(self, player_value: int) -> bool:
        """Check if the specified player has won."""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6],  # diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == player_value for i in condition):
                return True
        return False

    async def end_game(
        self, interaction: discord.Interaction, message: str
    ) -> None:
        """End the game and disable all buttons."""
        for item in self.children:
            item.disabled = True

        # Respond to the interaction that ended the game
        if not interaction.response.is_done():
            await interaction.response.edit_message(content=message, view=self)
        # If the interaction was already responded to (e.g., bot move), edit the original message
        else:
            await interaction.edit_original_response(content=message, view=self)
        self.stop()

    async def bot_move(self) -> None:
        """Handle the bot's move."""
        await asyncio.sleep(random.uniform(0.5, 1.5))  # Simulate thinking

        available_spots = [i for i, spot in enumerate(self.board) if spot == 0]
        if not available_spots:
            return

        bot_choice_pos = random.choice(available_spots)
        bot_button = next(
            item for item in self.children if isinstance(item, discord.ui.Button) and int(item.custom_id) == bot_choice_pos
        )

        self.board[bot_choice_pos] = 2  # Bot is always player 2
        bot_button.label = "O"
        bot_button.style = discord.ButtonStyle.danger
        bot_button.disabled = True

        if self.check_win(2):
            await self.end_game_from_bot(f"{self.current_player.mention} wins!")
            return

        if 0 not in self.board:
            await self.end_game_from_bot("It's a draw!")
            return

        self.current_player = self.player1
        await self.message.edit(
            content=f"It's {self.current_player.mention}'s turn.", view=self
        )

    async def end_game_from_bot(self, message: str) -> None:
        """Special version of end_game for when the bot makes the final move."""
        for item in self.children:
            item.disabled = True
        await self.message.edit(content=message, view=self)
        self.stop()


class TicTacToeButton(discord.ui.Button):
    """A button for the tic-tac-toe board."""

    async def callback(self, interaction: discord.Interaction):
        """Handle button press."""
        if self.view.board[int(self.custom_id)] != 0:
            await interaction.response.send_message(
                "This spot is already taken!", ephemeral=True
            )
            return
        await self.view.handle_turn(interaction, self)


class TicTacToe(commands.Cog):
    """Tic-tac-toe game commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Play a game of tic-tac-toe")
    async def tictactoe(
        self, ctx: commands.Context, member: discord.Member | None = None
    ) -> None:
        """Starts a tic-tac-toe game."""
        player1 = ctx.author
        player2 = member or self.bot.user

        if player2.bot and player2 != self.bot.user:
            await ctx.send("You cannot play against other bots.")
            return

        if player1 == player2:
            await ctx.send("You cannot play against yourself.")
            return

        view = TicTacToeView(self.bot, player1, player2)
        message = await ctx.send(
            f"Tic-tac-toe: {player1.mention} (X) vs {player2.mention} (O)\n"
            f"It's {view.current_player.mention}'s turn.",
            view=view,
        )
        view.message = message


async def setup(bot: commands.Bot) -> None:
    """Add the cog to the bot."""
    await bot.add_cog(TicTacToe(bot))
