import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        scammercheck = self.bot.db.fetchval('SELECT scammer from usercheck WHERE user_id = $1', member.id)
        if scammercheck is True:
            roles = await self.bot.db.fetchval('SELECT scammerrole from serverdata WHERE guild_id = $1', member.guild.id)
            role = discord.utils.get(member.guild.roles, id=roles)
            if role:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    print(f"{e}")
        dwccheck = self.bot.db.fetchval('SELECT dec from usercheck WHERE user_id = $1', member.id)
        if dwccheck is True:
            roles = await self.bot.db.fetchval('SELECT dwcrole from serverdata WHERE guild_id = $1', member.guild.id)
            role = discord.utils.get(member.guild.roles, id=roles)
            if role:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    print(f"{e}")

async def setup(bot):
    await bot.add_cog(Events(bot))