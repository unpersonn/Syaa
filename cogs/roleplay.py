import discord
from discord.ext import commands
import aiohttp  # Use aiohttp for asynchronous requests

API_URL = 'https://api.pawan.krd/cosmosrp/v1/chat/completions'
TEMPERATURE = 1.2
# Replace with your channel ID where the bot will respond
TARGET_CHANNEL_ID = 1299055695223853177  # Change this to your actual channel ID

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_cosmorp_response(self, behaviour: str, user_prompt: str):
        headers = {
            'Content-Type': 'application/json',
        }

        # Prepare messages in the required format
        data = {
            'model': 'cosmosrp',
            'messages': [
                {'role': 'system', 'content': behaviour},
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': TEMPERATURE
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    print(result)

                    if 'choices' in result and len(result['choices']) > 0:
                        return result['choices'][0]['message'].get('content', 'No content found in response.')
                    else:
                        return 'No choices found in the response.'
                else:
                    return f"Error: {response.status}, {await response.text()}"

    @commands.command(name="rp", help="Chat Roleplay")
    async def rp(self, ctx, *, prompt: str):
        behaviour = "Pretend you are a sexy sugar mommy, milf"
        response = await self.get_cosmorp_response(behaviour, prompt)
        await ctx.send(response)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself to avoid loops
        if message.author == self.bot.user:
            return

        # Check if the message is from the specified channel
        if message.channel.id == TARGET_CHANNEL_ID:
            behaviour = "Pretend you are a sexy sugar mommy, milf"
            user_prompt = message.content
            response = await self.get_cosmorp_response(behaviour, user_prompt)

            # Send the response back to the same channel
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(Roleplay(bot))