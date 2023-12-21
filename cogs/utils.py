import discord
from discord.ui import View, Button
from discord.ext import commands
from core.config import Configuration


class UtilCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, ctx):
        btn = Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1139082473918181416&permissions=8&scope=bot")
        view = View()
        view.add_item(btn)
        await ctx.send(view=view)

    @commands.command(name="support")
    async def support(self, ctx):
        btn = Button(label="Support", url="https://discord.gg/HseZKhjcAG")
        view=View()
        view.add_item(btn)
        await ctx.send(view=view)

    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(
            color= Configuration.Colors.default,
            description=f"**Ping : **`{int(self.bot.latency * 1000)}`ms")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilCmds(bot))