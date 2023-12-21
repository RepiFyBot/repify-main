import discord
from discord.ext import commands
from core.config import Configuration

class Help(commands.Cog):
    def __init__(self, bot):
        super().__init__()

    @commands.command(
        name="help"
    )
    async def help(self, ctx):
        e = discord.Embed(
            color=Configuration.Colors.default,
            title="Help Menu"
        )
        e.add_field(
            name="Bot",
            value=
            "**+help** - `shows this command`\n"
            "**+ping** - `shows the latency of this bot.`\n"
            "**+invite** - `shows the invite link for the bot`\n"
            "**+support** - `shows the support server link.`",
            inline= False
            )
        e.add_field(
            name="General",
            value=
            "**+profile** - `Displays your or mentioned user's profile`\n"
            "**+rep** - `Adds a positive vouch to the mentioned user.`\n"
            "**+token** - `Shows all the sub-commands of token`\n"
            "**+shop** - `Shows all the sub- commands of shop`",
            inline= False
        )
        e.add_field(
            name="Server",
            value="**+set** - `Shows all the sub - commands of set command`",
            inline=False
        )
        return await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Help(bot))