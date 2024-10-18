# cogs/fun.py
import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):
    def __init___(self,bot):
        self.bot = bot

    # coin flip
    @commands.command(name="flip", help="Flips a coin!")
    async def flip(self, ctx):
        message = await ctx.send("Flipping a coin...") # initial message
        await asyncio.sleep(3) # 2 second delay before simulating flip

        result = random.choice(["Heads", "Tails"])
        await message.edit(content=f"{result}!") # edit message with result

    # rock, paper, scissors
    @commands.command(name="rps", help="Play rock,paper,scissors with the bot")
    async def rps(self, ctx, user_choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)

        if user_choice.lower() not in choices:
            await ctx.send("Please choose rock, paper, or scissors!")
            return
        
        if user_choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (user_choice.lower() == 'rock' and bot_choice == 'scissors') or \
            (user_choice.lower() == 'paper' and bot_choice == 'rock') or \
            (user_choice.lower() == 'scissors' and bot_choice == 'paper'):
            result = 'You win!'
        else:
            result = 'You lose!'

        await ctx.send(f"You chose {user_choice}, I chose {bot_choice}, {result}.")

    
async def setup(bot):
    await bot.add_cog(Fun(bot))