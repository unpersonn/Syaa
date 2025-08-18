# Syaa – A Multi-Purpose Discord Bot

Syaa is a feature-packed Discord bot written in Python. It supports both
traditional prefix commands and modern slash commands, making it easy for
any server to integrate.

## Features

### Moderation
- `purge` – delete a specified number of messages.
- `timeout` – temporarily mute a member.
- `kick` – remove a member from the server.
- `ban` – ban a member from the server.

### Fun
- `flip` – flip a coin.
- `rps` – play rock, paper, scissors against the bot.

### Actions
Send a random animated GIF to interact with other members:
- `cuddle`
- `hug`
- `kiss`
- `bonk`
- `bully`
- `shoot`
- `pat`

### Math
- `calc` – evaluate a mathematical expression.

### Utility
- `/prefix` – show the bot's current prefix.

## Setup

1. **Install dependencies**
   ```bash
   pip install discord.py python-dotenv aiohttp
   ```
2. **Create a `.env` file** with the following content:
   ```env
   DISCORD_TOKEN=your_discord_token
   TENOR_API=your_tenor_api_key
   ```
3. **Run the bot**
   ```bash
   python main.py
   ```

Have fun!
