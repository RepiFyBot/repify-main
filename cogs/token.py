import discord
import string
import random

from core.config import Configuration
from discord.ext import commands


def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=70))

class TokenCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.group(
        invoke_without_command = True,
        name="token"
    )
    async def token(self, ctx):
        e = discord.Embed(
            color=Configuration.Colors.default,
            title=f"Valid SubCommands",
            description=f"`generate`"
        )
        return await ctx.send(embed=e)
    
    @token.group(
        name="generate"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tokengen(self, ctx):
        data = await self.bot.db.fetchval('SELECT token from token WHERE user_id = $1', ctx.author.id)
        if data:
            return await ctx.caution('A Token has already been generated for you.')
        else:
            token = generate_token()
            await self.bot.db.execute('INSERT INTO token(user_id, token) VALUES ($1, $2)', ctx.author.id, token)
            await ctx.success('Successfully Generated The Token. Check Your DM for more information.')
            e = discord.Embed(
                color=Configuration.Colors.default,
                description=f"{Configuration.Emoji.caution} **Rules**\n- Token Can only be generated Once. So keep this token safe.\n- You can Recover all your vouches from this token.\n- Keep this token Private Anyone with this can shift your vouches!"
            )
            e.add_field(name="Your Token:", value=f"```{token}```")
            await ctx.author.send(embed=e)

    @token.group(
        name="validate",
        aliases=["verify"]
    )
    async def validate(self, ctx, valitoken: str = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if valitoken is None:
                return await ctx.caution('Please Enter a Token to validate.')
            data = await self.bot.db.fetchrow('SELECT * FROM token WHERE token = $1', valitoken)
            user_id , token, used = data
            if token is True:
                return await ctx.error('This Token is already validated.')
            else:
                user = await self.bot.fetch_user(user_id)
                await self.bot.db.execute('INSERT INTO token(user_id, used) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET used = EXCLUDED.used', user_id, True)
                e = discord.Embed(
                    color=Configuration.Colors.default,
                    title="__Token Information__",
                    description=f"**User:** {user.name}\n**ID:** {user.id}"
                )
                e.set_footer(text='use +tp [user.id] [newuser.id] to tranfer the vouches.')
                return await ctx.send(embed=e)

    @commands.command(
        name="tp"
    )
    async def tranfervouches(self, ctx, old: discord.User = None, new: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if old is None:
                return await ctx.caution('Please Mention the user to transfer the vouches from.')
            if new is None:
                return await ctx.caution('Please Mention the user to transfer the vouches.')
            else:
                try:
                    await self.bot.db.execute('UPDATE vouches SET user_id = $1 WHERE user_id = $2', new.id, old.id)
                    await self.bot.db.execute('UPDATE shop SET user_id = $1 WHERE user_id = $2', new.id, old.id)
                except Exception as e:
                    print(f'{e}')
                await ctx.success(f'shifted all your configurations to {new.mention}')


async def setup(bot):
    await bot.add_cog(TokenCmds(bot))