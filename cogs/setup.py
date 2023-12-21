import discord
from discord.ext import commands
from core.config import Configuration


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
            invoke_without_command = True,
            name="set"
            )
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def set(self, ctx):
        e = discord.Embed(
            color=Configuration.Colors.default,
            title="Valid SubCommands",
            description="`scammer`, `dwc`, `logchannel`"
        )
        await ctx.send(embed=e)

    @set.group(
        name="scammer"
    )
    @commands.has_permissions(administrator=True)
    async def scammerset(self, ctx, role: discord.Role = None):
        if role is None:
            return await ctx.caution('Require Argument `role` is missing.')
        else:
            try:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id , scammerrole) VALUES ($1, $2)',  ctx.guild.id, role.id)
            except:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id, scammerrole) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET scammerrole = EXCLUDED.scammerrole', ctx.guild.id, role.id)
            await ctx.success(f'Successfully set {role.mention} as scammer role.')


    @set.group(
        name="dwc"
    )
    @commands.has_permissions(administrator=True)
    async def dwcset(self, ctx, role: discord.Role = None):
        if role is None:
            return await ctx.caution('Require Argument `role` is missing.')
        else:
            try:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id , dwcrole) VALUES ($1, $2)',  ctx.guild.id, role.id)
            except:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id, dwcrole) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET dwcrole = EXCLUDED.dwcrole', ctx.guild.id, role.id)
            await ctx.success(f'Successfully set {role.mention} as dwc role.')

    @set.group(
        name="logchannel",
        aliases=["logch"]
    )
    @commands.has_permissions(administrator=True)
    async def logchset(self, ctx, channel : discord.TextChannel):
        if channel is None:
            return await ctx.caution('Require Argument `channel` is missing.')
        else:
            try:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id , logch) VALUES ($1, $2)',  ctx.guild.id, channel.id)
            except:
                await self.bot.db.execute('INSERT INTO serverdata (guild_id, logch) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET logch = EXCLUDED.logch', ctx.guild.id, channel.id)
            await ctx.success(f'Successfully set {channel.mention} as logging channel.')
    


async def setup(bot):
    await bot.add_cog(Setup(bot))