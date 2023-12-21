import discord
from discord.ext import commands
from utils.Paginator import *
from core.config import Configuration

allowed_guilds = [1180549364117151875, 1180801914041012254]

class ListCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        invoke_without_command = True,
        name="pending"
    )
    @commands.cooldown(1 , 3, commands.BucketType.user)
    async def pending(self, ctx, user: discord.User = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            if user is None or user == "":
                user = ctx.author
            data = await self.bot.db.fetch('SELECT * FROM vouches WHERE user_id = $1 AND denied = False AND accepted = False AND manual_verify = False', user.id)
            if not data:
                return await ctx.warn('**There is No Pending vouches left.**')
            embeds = []
            pagenum = 0
            num = 0
            ret = []
            for num, data in enumerate(data, start=1):
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data
                ret.append(f'**{num}.** `{vouch_id}` - `{reason}`')
                pages = [p for p in discord.utils.as_chunks(ret, 10)]
            for page in pages:
                pagenum += 1
                embeds.append(discord.Embed(
                    color=Configuration.Colors.default,
                    title=f'Pending Vouches for {user.name}',
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
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')

    
    @pending.group(
        name="all"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pendingall(self, ctx):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            vouch_data_rows = await self.bot.db.fetch('SELECT * FROM vouches WHERE denied = False AND accepted = False AND manual_verify = False')
            if not vouch_data_rows:
                return await ctx.warn('There Are No Pending Vouches Left.')
            embeds = []
            pagenum = 0
            num = 0
            ret = []
            for num, data_row in enumerate(vouch_data_rows, start=1):
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data_row
                vouchuser = await self.bot.fetch_user(user_id)
                ret.append(f'**{num}.** - {vouchuser.name} - `{vouch_id}` - `{reason}`')
            pages = [p for p in discord.utils.as_chunks(ret, 10)]
            for page in pages:
                pagenum += 1
                embeds.append(discord.Embed(
                    color=Configuration.Colors.default,
                    title=f'Pending Vouches in RepiFy',
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
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')
        

async def setup(bot):
    await bot.add_cog(ListCmds(bot))