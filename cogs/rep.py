import discord
import random
import time 
import string
from core.config import Configuration
from discord.ext import commands


def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def contains_numerical_values(input_string):
    for char in input_string:
        if char.isdigit():
            return True
    return False

class Vouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="rep",
        aliases=["vouch"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def vouch(self, ctx, user: discord.User = None, *, reason : str = None, amt : int = None):
        if user is None:
            return await ctx.warn('Please mention a user to vouch.')
        if user == ctx.author:
            return await ctx.caution('You can\'t vouch yourself.')
        if reason is None:
            return await ctx.warn('Vouch Reason cannot be empty.')
        scammer = await self.bot.db.fetchval('SELECT scammer FROM usercheck WHERE user_id = $1', user.id)
        scammerreason = await self.bot.db.fetchval('SELECT scammer_reason FROM usercheck WHERE user_id = $1', user.id)
        if scammer is True:
            e = discord.Embed(
                    color=Configuration.Colors.error,
                    title="Marked By RepiFy Staff"
                )
            e.set_author(name=f"{user.name} is a Scammer")
            e.add_field(name="This user was Marked for:", value=f"{scammerreason}" ,inline=False)
            return await ctx.send(embed=e)
        blacklisted = await self.bot.db.fetchval('SELECT blacklisted FROM usercheck WHERE user_id = $1', user.id)
        if blacklisted is True:
            embed = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} **Blacklisted From Vouches.**",
                description="This user is blacklisted by the RepiFy Staffs."
            )
            return await ctx.send(embed=embed)
        try:
            if contains_numerical_values(reason):
                pass
            else:
                e = discord.Embed(
                    color=Configuration.Colors.error,
                    description=f"<:error:1180159425776975942> {ctx.author.mention} : **Your Vouch Was automatically denied for not specifying the price of what you were vouching for.**"
                )
                e.set_footer(text="RepiFy")
                return await ctx.send(embed=e)
        except:
            return
        else:
            log_server = self.bot.get_guild(1180801914041012254)
            logch = discord.utils.get(log_server.channels, id=1180802111068459089)
            vouchid = generate_verification_code()
            tame = int(time.time())
            await self.bot.db.execute('INSERT INTO vouches(user_id , vouch_id, time, vouchby, reason) VALUES ($1, $2, $3, $4, $5)', user.id, vouchid, f"{tame}", ctx.author.id, reason)
            await ctx.success(f'Successfully Gave a positive vouch to {user.mention}')
            dm = discord.Embed(
                color=Configuration.Colors.default,
                title="Vouch Notifier",
                description=f"You have recieved a positive vouch from `{ctx.author.name}`. The ID of this vouch is `{vouchid}`"
            )
            await user.send(embed=dm)
            e = discord.Embed(
                color=Configuration.Colors.default,
                title=f"Vouch ID: {vouchid}",
                description=
                f"**Recipient Tag:** {user.name}\n"
                f"**Recipient ID:** {user.id}\n\n"
                f"**Giver Tag:** {ctx.author.name}\n"
                f"**Giver ID:** {ctx.author.id}\n\n"
                f"**Vouch Type:** Positive\n\n"
                f"**Comment:** {reason}\n\n"
            )
            e.set_footer(text=f"+approve {vouchid} | +deny {vouchid}")
            await logch.send(embed=e)



async def setup(bot):
    await bot.add_cog(Vouch(bot))