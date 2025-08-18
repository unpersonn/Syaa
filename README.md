# Syaa - A multi-purpose Discord Bot!

- My first discord bot.
- Features multiple funcitonalities such as moderation commands, fun mini-games and actions.
- Made in python!

## Prefix configuration

Syaa supports a per-guild command prefix stored in a local SQLite database.  Use
the following slash commands to manage it:

- `/prefix` - show the current prefix for the guild
- `/setprefix <prefix>` - set a custom prefix (administrator only)
- `/resetprefix` - remove the custom prefix and revert to the default `!`
