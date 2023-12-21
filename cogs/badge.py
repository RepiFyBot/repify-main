import discord
from discord.ext import commands
import json
from typing import Optional, Union

class BadgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_badges()

    def load_badges(self):
        try:
            with open("./schemas/badges.json", "r") as f:
                self.badges = json.load(f)
        except FileNotFoundError:
            self.badges = {}

    def save_badges(self):
        with open("./schemas/badges.json", "w") as f:
            json.dump(self.badges, f, indent=4)


    @commands.command()
    @commands.is_owner()
    async def addbadge(self, ctx, user: discord.Member = None, *,badge_name: str = None):
        if user is None:
            return await ctx.error('Please Mention a user to add badge')
        if badge_name is None:
            return await ctx.caution('Please Enter your badge name.')
        if str(user.id) not in self.badges:
            self.badges[str(user.id)] = []
        self.badges[str(user.id)].append(badge_name)
        self.save_badges()
        await ctx.send(f"Added '{badge_name}' badge to {user.display_name}.")

    @commands.command()
    @commands.is_owner()
    async def removebadge(self, ctx, user: discord.Member = None, *,badge_name: str = None):
        if user is None:
            return await ctx.error('Please Mention a user to remove badge')
        if badge_name is None:
            return await ctx.caution('Please Enter your badge name.')
        if str(user.id) in self.badges and badge_name in self.badges[str(user.id)]:
            self.badges[str(user.id)].remove(badge_name)
            self.save_badges()
            await ctx.send(f"Removed '{badge_name}' badge from {user.display_name}.")
        else:
            await ctx.send(f"{user.display_name} doesn't have the '{badge_name}' badge.")

    @commands.command(name="badges")
    async def _badges(self, ctx, user: Optional[Union[discord.Member, discord.User]] = None):
        if user == None or user == "":
            user = ctx.author
        if str(user.id) in self.badges:
            badges_str = "\n".join(self.badges[str(user.id)])
            embed = discord.Embed(color=0x0E1CF1, description=f"{badges_str}")
            embed.set_author(name=f"Badges of {user.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{user.display_name} doesn't have any badges.")

async def setup(bot):
    await bot.add_cog(BadgeCog(bot))