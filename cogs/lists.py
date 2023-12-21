import discord
from discord.ext import commands
from core.config import Configuration
from utils.Paginator import Paginator

allowed_guilds = [1162074777436028928, 1133364060491104266]


class listCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(
        invoke_without_command = True,
        name="list"
    )
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list(self, ctx):
        e = discord.Embed(
            color=Configuration.Colors.default,
            title="Valid SubCommands",
            description="`admins`, `staff`, `noprefix`"
        )
        return await ctx.send(embed=e)
    

    @list.group(
        name="admins"
    )
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def listadmins(self, ctx):
        data = await self.bot.db.fetch('SELECT * from staffs WHERE vouchadmin = True')
        if not data:
            return await ctx.error('There are no user with admin privileges.')
        embeds = []
        pagenum = 0
        num = 0
        ret = []
        for num, data_row in enumerate(data, start=1):
            user_id, noprefix, vouchadmin, vouchstaff= data_row
            admins = await self.bot.fetch_user(user_id)
            ret.append(f'**{num} .** - ``{admins.name}`` - ``({admins.id})``')
        pages = [p for p in discord.utils.as_chunks(ret, 10)]
        for page in pages:
            pagenum += 1
            embeds.append(
                discord.Embed(
                    color=Configuration.Colors.default,
                    title="Admins List In RepiFy",
                    description="\n".join(page))
                    .set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    .set_footer(text=f'Page {pagenum}/{len(pages)}')
                )
        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
        else:
            pag = Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
            pag.add_button('prev', emoji='<:arrow_left1:1114813373335474256>')
            pag.add_button('delete', emoji='<:deleteeeee:1112424613285220384>')
            pag.add_button('next', emoji='<:icons_rightarrow:1114813386224566293>')
            await pag.start()
            

    @list.group(
        name="staff"
    )
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def liststaff(self, ctx):
        data = await self.bot.db.fetch('SELECT * from staffs WHERE vouchstaff = True')
        if not data:
            return await ctx.error('There are no user with staff privileges.')
        embeds = []
        pagenum = 0
        num = 0
        ret = []
        for num, data_row in enumerate(data, start=1):
            user_id, noprefix, vouchadmin, vouchstaff= data_row
            staff = await self.bot.fetch_user(user_id)
            ret.append(f'**{num} .** - ``{staff.name}`` - ``({staff.id})``')
        pages = [p for p in discord.utils.as_chunks(ret, 10)]
        for page in pages:
            pagenum += 1
            embeds.append(
                discord.Embed(
                    color=Configuration.Colors.default,
                    title="Staff List In RepiFy",
                    description="\n".join(page))
                    .set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    .set_footer(text=f'Page {pagenum}/{len(pages)}')
                )
        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
        else:
            pag = Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
            pag.add_button('prev', emoji='<:arrow_left1:1114813373335474256>')
            pag.add_button('delete', emoji='<:deleteeeee:1112424613285220384>')
            pag.add_button('next', emoji='<:icons_rightarrow:1114813386224566293>')
            await pag.start()


    @list.group(
        name="noprefix",
        aliases=["np"]
    )
    @commands.is_owner()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def liststaff(self, ctx):
        data = await self.bot.db.fetch('SELECT * from staffs WHERE noprefix = True')
        if not data:
            return await ctx.error('There are no Noprefix users.')
        embeds = []
        pagenum = 0
        num = 0
        ret = []
        for num, data_row in enumerate(data, start=1):
            user_id, noprefix, vouchadmin, vouchstaff= data_row
            staff = await self.bot.fetch_user(user_id)
            ret.append(f'**{num} .** - ``{staff.name}`` - ``({staff.id})``')
        pages = [p for p in discord.utils.as_chunks(ret, 10)]
        for page in pages:
            pagenum += 1
            embeds.append(
                discord.Embed(
                    color=Configuration.Colors.default,
                    title="Noprefix List In RepiFy",
                    description="\n".join(page))
                    .set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    .set_footer(text=f'Page {pagenum}/{len(pages)}')
                )
        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
        else:
            pag = Paginator(self.bot, embeds, ctx, invoker=ctx.author.id)
            pag.add_button('prev', emoji='<:arrow_left1:1114813373335474256>')
            pag.add_button('delete', emoji='<:deleteeeee:1112424613285220384>')
            pag.add_button('next', emoji='<:icons_rightarrow:1114813386224566293>')
            await pag.start()



async def setup(bot):
    await bot.add_cog(listCmds(bot))