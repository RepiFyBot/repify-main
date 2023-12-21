import discord
from discord.ext import commands
from core.config import Configuration

class TopCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
        name="top"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top(self, ctx):
        data = await self.bot.db.fetch("SELECT user_id, SUM(vouches + imported) AS total_count FROM usercheck GROUP BY user_id ORDER BY total_count DESC LIMIT 10")
        top_ten = []
        for idx, (user_id, total_count) in enumerate(data, start=1):
            user = await self.bot.fetch_user(user_id)
            top_ten.append(f"**{idx}.** {user.name} : **{total_count}** vouches")

        e = discord.Embed(
            color= Configuration.Colors.default,
            title="Top 10 Users of RepiFy are:",
            description="\n".join(top_ten),
            )
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(TopCmd(bot))