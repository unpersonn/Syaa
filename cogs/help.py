import discord
from discord.ext import commands
from utils.ui import SyaaEmbed, COLOR_MAIN

class HelpSelect(discord.ui.Select):
    """Dropdown menu for selecting help categories."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Home",
                description="Return to the main help page",
                emoji="🏠",
                value="home"
            ),
            discord.SelectOption(
                label="Moderation",
                description="Tools for server management",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="Fun",
                description="Games and recreational commands",
                emoji="🎉",
                value="fun"
            ),
            discord.SelectOption(
                label="Actions",
                description="Interactions like hug, kiss, pat",
                emoji="🤗",
                value="actions"
            ),
            discord.SelectOption(
                label="Games",
                description="Hangman, TicTacToe, etc.",
                emoji="🎮",
                value="games"
            ),
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        
        if value == "home":
             embed = self.view.get_home_embed()
        else:
             embed = self.get_category_embed(value)
        
        await interaction.response.edit_message(embed=embed, view=self.view)

    def get_category_embed(self, category: str) -> discord.Embed:
        embed = SyaaEmbed(title=f"{category.title()} Commands")
        
        # Mapping categories to Cog names properly
        cog_mapping = {
            "moderation": "Moderation",
            "fun": "Fun",
            "actions": "Actions",
            "games": ["Hangman", "TicTacToe"] # Special handling for multiple cogs
        }

        target = cog_mapping.get(category)
        commands_list = []

        if isinstance(target, list):
             for t in target:
                 cog = self.bot.get_cog(t)
                 if cog:
                     for cmd in cog.get_commands():
                        if not cmd.hidden:
                             commands_list.append(cmd)
        elif target:
            cog = self.bot.get_cog(target)
            if cog:
                commands_list = cog.get_commands()

        if commands_list:
            for cmd in commands_list:
                # Use slash command mention if possible, else prefix
                signature = f"/{cmd.name}" if isinstance(cmd, commands.HybridCommand) else f"!{cmd.name}"
                embed.add_field(
                    name=f"`{signature}`",
                    value=cmd.description or "No description provided.",
                    inline=False
                )
        else:
            embed.description = "No commands found in this category."

        return embed


class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot, user: discord.User):
        super().__init__(timeout=180)
        self.bot = bot
        self.user = user
        self.add_item(HelpSelect(bot))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return False
        return True
    
    def get_home_embed(self) -> discord.Embed:
        embed = SyaaEmbed(
            title="✨ Syaa Help Center",
            description=(
                "Welcome to **Syaa**! A multi-purpose bot designed for fun and style.\n\n"
                "📂 **Browse Commands**\n"
                "Use the dropdown menu below to view specific categories.\n\n"
                "❓ **Support**\n"
                "If you find a bug or need help, contact the developer."
            )
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_image(url="https://media.tenor.com/PshgR1u72QcAAAAC/anime-welcome.gif") # Placeholder aesthetic banner
        embed.set_footer(text=f"Requested by {self.user.display_name}", icon_url=self.user.display_avatar.url)
        return embed


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Show the help menu.")
    async def help(self, ctx: commands.Context):
        view = HelpView(self.bot, ctx.author)
        embed = view.get_home_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
