import discord
import json
import asyncio
from discord.ext import commands
from core.config import Configuration
from discord.utils import format_dt


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_badges(self):
        try:
            with open("./schemas/badges.json", "r") as f:
                self.badges = json.load(f)
        except FileNotFoundError:
            self.badges = {}

    def save_badges(self):
        with open("./schemas/badges.json", "w") as f:
            json.dump(self.badges, f, indent=4)

    @commands.command(
        name="profile",
        aliases=["pr", "p"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, user: discord.User = None):
        if user is None or user == "":
            user = ctx.author
        data = await self.bot.db.fetchrow('SELECT * from usercheck WHERE user_id = $1', user.id)
        if data is not None:
            user_id , vouches, imported, scammer, dwc, blacklisted, scammer_reason = data
        else:
            pass
        shop = await self.bot.db.fetchrow('SELECT * from shop WHERE user_id = $1', user.id)
        color = None
        if shop is not None:
            user_id, shop, img, forum, product, color = shop
        else:
            pass
        if not data:
            created_at = user.created_at
            formatted_created_at = format_dt(created_at, style="f")
            if color is None:
                emcolor = Configuration.Colors.default
            else:
                emcolor = discord.Color(int(color, 16))
            e = discord.Embed(color=emcolor)
            e.add_field(
                name="__Information___",
                value=
                f"**ID :** {user.id}\n"
                f"**Name :** {user.name}\n"
                f"**Mention :** {user.mention}\n"
                f"**Registered On:** {formatted_created_at}\n"
                )
            e.add_field(name="__Vouch Information__", value=f"**Positive :** 0\n**Imported :** 0\n**Overall :** 0", inline=False)
            e.set_author(name=f"{user.name}", icon_url=f"{user.display_avatar.url}")
            try:
                if str(user.id) in self.badges:
                    badges_str = "\n".join(self.badges[str(user.id)])
                e.add_field(name="__Badges__", value=f"{badges_str}", inline=False)
            except:
                e.add_field(name="Badges", value="This User has No badges", inline=False)

            try:
                if not img:
                    pass
                else:
                    e.set_image(url=f"{img}")
            except:
                pass
            try:
                if not shop:
                    e.add_field(name="Shop", value="None", inline=False)
                else:
                    e.add_field(name="Shop", value=f"Link : https://discord.gg/{shop}", inline=False)
            except:
                pass
            try:
                e.add_field(name="Products", value=f"{product}", inline=False)
            except:
                e.add_field(name="Products", value="Set This !", inline=False)
            try:
                e.add_field(name="Forum", value=f"{forum}", inline=False)
            except:
                e.add_field(name="Forum", value=f"Set This!", inline=False)
            e.add_field(name="__Past 5 Comments__", value=f"This User has no vouches yet.", inline=False)
            e.set_footer(text="discord.gg/repify")
            lol = await ctx.send(embed=e)
            await asyncio.sleep(20)
            await lol.delete()
            return
        if scammer is True:
            e = discord.Embed(
                color=Configuration.Colors.error,
                title="Marked By RepiFy Staff"
            )
            e.add_field(name="This user was Marked for:", value=f"{scammer_reason}")
            e.set_author(name=f"{user.name} is a scammer")
            return await ctx.send(embed=e)
        if blacklisted is True:
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title="Blacklisted By RepiFy Staff",
                description="**This user has been blacklisted from using RepiFy due to RepiFy ToS violation.**"
            )
            e.set_author(name=f"{user.name} is Blacklisted.")
            return await ctx.send(embed=e)
        if dwc is True:
            created_at = user.created_at
            formatted_created_at = format_dt(created_at, style="f")
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} DEAL WITH CAUTION {Configuration.Emoji.caution}",
                description="**Reason:** Middleman Refusal"
            )
            e.add_field(
                name="__Information___",
                value=
                f"**ID :** {user.id}\n"
                f"**Name :** {user.name}\n"
                f"**Mention :** {user.mention}\n"
                f"**Registered On:** {formatted_created_at}\n"
                )
            e.add_field(
                name="__Vouch Information__",
                value=
                f"**Positive :** {vouches}\n"
                f"**Imported :** {imported}\n"
                f"**Overall :** {vouches + imported}",
                inline=False)
            e.set_author(name=f"{user.name}", icon_url=f"{user.display_avatar.url}")
            try:
                if str(user.id) in self.badges:
                    badges_str = "\n".join(self.badges[str(user.id)])
                e.add_field(name="__Badges__", value=f"{badges_str}", inline=False)
            except:
                e.add_field(name="Badges", value="This User has No badges", inline=False)

            try:
                if not img:
                    pass
                else:
                    e.set_image(url=f"{img}")
            except:
                pass
            try:
                if not shop:
                    e.add_field(name="Shop", value="None", inline=False)
                else:
                    e.add_field(name="Shop", value=f"Link : https://discord.gg/{shop}", inline=False)
            except:
                pass
            try:
                e.add_field(name="Products", value=f"{product}", inline=False)
            except:
                e.add_field(name="Products", value="Set This !", inline=False)
            try:
                e.add_field(name="Forum", value=f"{forum}", inline=False)
            except:
                e.add_field(name="Forum", value=f"Set This!", inline=False)
            try:
                vouch_data = await self.bot.db.fetch("SELECT reason FROM vouches WHERE user_id = $1 AND accepted = True LIMIT 5", user.id)
                vouch_list = "\n".join([f"{index + 1}. {vouch['reason']}" for index, vouch in enumerate(vouch_data)])
                e.add_field(name="__Past 5 Comments__", value=f"{vouch_list}", inline=False)
            except Exception as err:
                print(err)
                e.add_field(name="__Past 5 Comments__", value=f"This User has no vouches yet.", inline=False)
            e.set_footer(text="discord.gg/repify")
            lol = await ctx.send(embed=e)
            await asyncio.sleep(20)
            await lol.delete()
            return
        else:
            created_at = user.created_at
            formatted_created_at = format_dt(created_at, style="f")
            if color is None:
                emcolor = Configuration.Colors.default
            else:
                emcolor = discord.Color(int(color, 16))
            e = discord.Embed(color=emcolor)
            e.add_field(
                name="__Information___",
                value=
                f"**ID :** {user.id}\n"
                f"**Name :** {user.name}\n"
                f"**Mention :** {user.mention}\n"
                f"**Registered On:** {formatted_created_at}\n"
                )
            e.add_field(
                name="__Vouch Information__",
                value=
                f"**Positive :** {vouches}\n"
                f"**Imported :** {imported}\n"
                f"**Overall :** {vouches + imported}",
                inline=False)
            e.set_author(name=f"{user.name}", icon_url=f"{user.display_avatar.url}")
            try:
                if str(user.id) in self.badges:
                    badges_str = "\n".join(self.badges[str(user.id)])
                e.add_field(name="__Badges__", value=f"{badges_str}", inline=False)
            except:
                e.add_field(name="Badges", value="This User has No badges", inline=False)

            try:
                if not img:
                    pass
                else:
                    e.set_image(url=f"{img}")
            except:
                pass
            try:
                if not shop:
                    e.add_field(name="Shop", value="None", inline=False)
                else:
                    e.add_field(name="Shop", value=f"Link : https://discord.gg/{shop}", inline=False)
            except:
                pass
            try:
                e.add_field(name="Products", value=f"{product}", inline=False)
            except:
                e.add_field(name="Products", value="Set This !", inline=False)
            try:
                e.add_field(name="Forum", value=f"{forum}", inline=False)
            except:
                e.add_field(name="Forum", value=f"Set This!", inline=False)
            try:
                vouch_data = await self.bot.db.fetch("SELECT reason FROM vouches WHERE user_id = $1 AND accepted = True LIMIT 5", user.id)
                vouch_list = "\n".join([f"{index + 1}. {vouch['reason']}" for index, vouch in enumerate(vouch_data)])
                e.add_field(name="__Past 5 Comments__", value=f"{vouch_list}", inline=False)
            except Exception as err:
                print(err)
#                e.add_field(name="__Past 5 Comments__", value=f"This User has no vouches yet.", inline=False)
            e.set_footer(text="discord.gg/repify")
            lol = await ctx.send(embed=e)
            await asyncio.sleep(20)
            await lol.delete()
            return

async def setup(bot):
    await bot.add_cog(Profile(bot))