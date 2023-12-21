import discord
from discord.ext import commands
from core.config import Configuration

allowed_guilds = [1180549364117151875, 1180801914041012254]

class StaffCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="fetch",
        aliases=['get']
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _get(self, ctx, vouchid : str = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            if vouchid is None:
                return await ctx.caution('Please Enter a Vouch ID.')
            data = await self.bot.db.fetchrow('SELECT * FROM vouches WHERE vouch_id = $1', vouchid)
            if data is not None:
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data
                vouchuser = await self.bot.fetch_user(user_id)
                vouchedby = await self.bot.fetch_user(vouchby)
                e = discord.Embed(
                    color=Configuration.Colors.default,
                    title=f"Vouch ID: {vouch_id}",
                    description=
                    f"**Recipient Tag:** {vouchuser.name}\n"
                    f"**Recipient ID:** {vouchuser.id}\n\n"
                    f"**Giver Tag:** {vouchedby.name}\n"
                    f"**Giver ID:** {vouchedby.id}\n\n"
                    f"**Vouch Type:** Positive\n"
                    f"**When:** <t:{time}:f>\n"
                    f"**Comment :** {reason}"
                    )
                if accepted is True:
                    e.add_field(name="Status", value="<:success:1159896689239400549> **>** Approved.")
                if denied is True:
                    e.add_field(name="Status", value="<:error:1159896678481006604> **>** Declined.", inline=False)
                    e.add_field(name="Decline Reason", value=f">>> {denyreason}", inline=False)
                if manual_verify is True:
                    e.add_field(name="Status", value="<:warning:1159896699611914320> **>** On Manaul Verification")
                if accepted is False and manual_verify is False and denied is False:
                    e.add_field(name="Status", value="<:warning:1159896699611914320> **>** Not Checked Yet")
                await ctx.send(embed=e)
            else:
                await ctx.warn(f'**There\'s No vouch exists with the ID : `{vouchid}`**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')
        

    @commands.command(
        name="accept",
        aliases=["a"]
    )
    async def accept(self, ctx, *, vouchid : str = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            logserver = self.bot.get_guild(1180801914041012254)
            logch = discord.utils.get(logserver.channels, id=1180804179254587432)
            if vouchid is None:
                return await ctx.error('**Please Enter a vouch ID.**')
            data = await self.bot.db.fetchrow('SELECT * FROM vouches WHERE vouch_id = $1', vouchid)
            if data is not None:
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data
                if user_id == ctx.author.id:
                    return await ctx.error('Heyy Staff. Kindly ask any other staff member to verify your vouch.')
                if accepted is True:
                    return await ctx.error('**This vouch is already Verified by the RepiFy Staff.**')
                if denied is True:
                    return await ctx.error('**This Vouch has been Declined by the RepiFy staff.**')
                else:
                    vouchto = await self.bot.fetch_user(user_id)
                    vouchby = await self.bot.fetch_user(vouchby)
                    await self.bot.db.execute('INSERT INTO vouches (vouch_id, accepted, manual_verify) VALUES ($1, $2, $3) ON CONFLICT (vouch_id) DO UPDATE SET accepted = EXCLUDED.accepted, manual_verify = EXCLUDED.manual_verify', vouchid, True, False)
                    await ctx.success(f"Successfully Accepted **{vouchto.name}'s** vouch with **ID: `{vouchid}`**")
                    dmem = discord.Embed(
                        color=Configuration.Colors.default,
                        title="Vouch Verification System",
                        description=f"**Your vouch with the ID : `{vouchid}` was approved.**"
                    )
                    dmem.set_footer(text="RepiFy | discord.gg/repify")
                    await vouchto.send(embed=dmem)
                    logem = discord.Embed(
                        color=Configuration.Colors.success,
                        title=f"Vouch ID : {vouch_id}",
                        description=
                        f"**Recipient Tag:** {vouchto.name}\n"
                        f"**Recipient ID:** {vouchto.id}\n\n"
                        f"**Giver Tag:** {vouchby.name}\n"
                        f"**Giver ID:** {vouchby.id}\n\n"
                        f"**Vouch Type:** Positive\n\n"
                        f"**Comment :** {reason}"
                    )
                    logem.set_footer(text=f"approved by {ctx.author.name}")
                    await logch.send(embed=logem)
                    olddata = await self.bot.db.fetchval('SELECT vouches from usercheck WHERE user_id = $1', user_id)
                    if not olddata:
                        newdata = 1
                    else:
                        newdata = olddata + 1
                    try:
                        await self.bot.db.execute('INSERT INTO usercheck (user_id, vouches) VALUES ($1, $2)', user_id, newdata)
                    except:
                        await self.bot.db.execute('INSERT INTO usercheck (user_id, vouches) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET vouches = EXCLUDED.vouches', user_id, newdata)
            else:
                await ctx.warn(f'**There\'s No vouch exists with the ID : `{vouchid}`**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')



    @commands.command(
        name="deny",
        aliases=["d", "decline"]
    )
    async def deny(self, ctx, vouchid: str, *,dreason: str = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            logserver = self.bot.get_guild(1180801914041012254)
            logch = discord.utils.get(logserver.channels, id=1180804193083215912)
            if dreason is None:
                dreason = 'No Reason Provided.'
            if dreason == "lowamount" or dreason == "Lowsamount":
                dreason = 'The Vouch Cannot Be Accepted Because The Amount Of This Vouch Is Below .5$/45₹'
            if dreason == "Incorrect" or dreason == "incorrect":
                dreason = "This Vouch Cannot Be Accepted Because It Does Not Contains Proper  Details Please Revouch And Specify More Details"
            if dreason == "bot" or dreason == "Bot":
                dreason = "This Vouch Cannot Be Accepted Because It Contains Bot Currency"
            if dreason == "ns" or dreason == "Ns":
                dreason = "This Vouch Cannot Be Accepted Because It Contains Items that are against discord tos"
            if dreason == "duplicate" or dreason == "Duplicate":
                dreason = "This Vouch Cannot Be Accepted Because It Is a duplicate vouch"
            data = await self.bot.db.fetchrow('SELECT * FROM vouches WHERE vouch_id = $1', vouchid)
            if data is not None:
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data
                if accepted is True:
                    return await ctx.error('**This vouch is Verified by the RepiFy Staff.**')
                if denied is True:
                    return await ctx.error('**This Vouch has already been Declined by the RepiFy staff.**')
                else:
                    vouchto = await self.bot.fetch_user(user_id)
                    vouchby = await self.bot.fetch_user(vouchby)
                    await self.bot.db.execute('INSERT INTO vouches (vouch_id, denied, denyreason) VALUES ($1, $2, $3) ON CONFLICT (vouch_id) DO UPDATE SET denied = EXCLUDED.denied, denyreason = EXCLUDED.denyreason', vouchid, True, dreason)
                    await ctx.success(f"Successfully Declined  **{vouchto.name}'s** vouch with **ID: `{vouchid}`**")
                    dmem = discord.Embed(
                        color=Configuration.Colors.default,
                        title="Vouch Verification System",
                        description=f"**Your vouch with the ID : `{vouchid}` was declined because `{dreason}`.**"
                    )
                    dmem.set_footer(text="RepiFy | discord.gg/repify")
                    await vouchto.send(embed=dmem)
                    logem = discord.Embed(
                        color=Configuration.Colors.error,
                        title=f"Vouch ID : {vouch_id}",
                        description=
                        f"**Recipient Tag:** {vouchto.name}\n"
                        f"**Recipient ID:** {vouchto.id}\n\n"
                        f"**Giver Tag:** {vouchby.name}\n"
                        f"**Giver ID:** {vouchby.id}\n\n"
                        f"**Vouch Type:** Positive\n\n"
                        f"**Comment :** {reason}\n"
                        f"**Denial Reason:** {dreason}"
                    )
                    logem.set_footer(text=f"declined by {ctx.author.name}")
                    await logch.send(embed=logem)
            
            else:
                await ctx.warn(f'**There\'s No vouch exists with the ID : `{vouchid}`**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')



    @commands.command(
        name="verify",
        aliases=["v"]
    )
    async def verify(self, ctx, *, vouchid : str = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            logserver = self.bot.get_guild(1180801914041012254)
            logch = discord.utils.get(logserver.channels, id=1180804205741604864)
            if vouchid is None:
                return await ctx.error('**Please Enter a vouch ID.**')
            data = await self.bot.db.fetchrow('SELECT * FROM vouches WHERE vouch_id = $1', vouchid)
            if data is not None:
                user_id, vouch_id, time, vouchby, reason, accepted, denied, manual_verify, denyreason = data
                if accepted is True:
                    return await ctx.error('**This vouch is Verified by the RepiFy Staff.**')
                if denied is True:
                    return await ctx.error('**This Vouch has been Declined by the RepiFy staff.**')
                else:
                    vouchto = await self.bot.fetch_user(user_id)
                    vouchby = await self.bot.fetch_user(vouchby)
                    await self.bot.db.execute('INSERT INTO vouches (vouch_id, manual_verify) VALUES ($1, $2) ON CONFLICT (vouch_id) DO UPDATE SET manual_verify = EXCLUDED.manual_verify', vouchid, True)
                    await ctx.success(f"Successfully Put **{vouchto.name}'s** vouch with **ID: `{vouchid}` Under Manual Verification.**")
                    dmem = discord.Embed(
                        color=Configuration.Colors.default,
                        title="Vouch Verification System",
                        description=f"You have recieved the positive vouch `{vouch_id}` from `{vouchby.name}`. This vouch requires manual verification by a staff member. Please join the [repify Support Server](https://discord.gg/repify) and open a ticket to provide proof for the vouch.If a ticket is not opened within 2 days, this vouch will be denied.\nShould this happen more regularly, you might get blacklisted from our vouch-system."
                    )
                    dmem.set_footer(text="RepiFy | discord.gg/repify")
                    await vouchto.send(embed=dmem)
                    logem = discord.Embed(
                        color=Configuration.Colors.success,
                        title=f"Vouch ID : {vouch_id}",
                        description=
                        f"**Recipient Tag:** {vouchto.name}\n"
                        f"**Recipient ID:** {vouchto.id}\n\n"
                        f"**Giver Tag:** {vouchby.name}\n"
                        f"**Giver ID:** {vouchby.id}\n\n"
                        f"**Vouch Type:** Positive\n\n"
                        f"**Comment :** {reason}"
                    )
                    logem.set_footer(text=f"managed by {ctx.author.name}")
                    await logch.send(embed=logem)
            else:
                await ctx.warn(f'**There\'s No vouch exists with the ID : `{vouchid}`**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a staff to use this command.')

    @commands.command(
        name="dm",
    )
    async def dm(self, ctx, user: discord.User = None):
        staffcheck = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', ctx.author.id)
        if staffcheck is True and ctx.guild.id in allowed_guilds:
            if user is None:
                return await ctx.error('Please Mention a user.')
            else:
                await user.send("""Hello,
We have a report open against you within RepiFy. Please join the server within 12h hours or you may be listed as a scammer or DWC.
Ping Any Report Mod to Add you in the ticket.

Server : https://discord.gg/repify""")


async def setup(bot):
    await bot.add_cog(StaffCmds(bot))