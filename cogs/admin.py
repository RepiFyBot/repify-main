import discord

from discord.ext import commands
from core.config import Configuration
from typing import Union
from discord.ui import Button, View

class AdminCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(
        invoke_without_command = True,
        name="scammer"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def scammer(self, ctx):
        return await ctx.caution('Please Enter a valid argument `[ add / remove ]`')
    
    @scammer.group(
        name="add"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def scammeradd(self, ctx, user: discord.User = None, *, reason : str = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to mark as scammer.')
            if user == ctx.author:
                return await ctx.error('You cannot mark yourself as scammer.')
            if reason is None:
                reason = "No Reason Provided."
            data = await self.bot.db.fetchval('SELECT scammer FROM usercheck WHERE user_id = $1', user.id)
            if data is True:
                return await ctx.caution(f'**{user.name}** has already been marked as scammer.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , scammer , scammer_reason) VALUES ($1 , $2, $3)', user.id, True, reason)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, scammer, scammer_reason) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET scammer = EXCLUDED.scammer, scammer_reason = EXCLUDED.scammer_reason', user.id, True, reason)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} Scammer Marked.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                            for guild in self.bot.guilds:
                                    if user in guild.members:
                                        member = guild.get_member(user.id)
                                        guildscammerrole = await self.bot.db.fetchval('SELECT scammerrole from serverdata WHERE guild_id = $1', guild.id)
                                        role_to_assign = guild.get_role(guildscammerrole)
                                        if role_to_assign:
                                            try:
                                                await member.add_roles(role_to_assign)
                                            except Exception as e:
                                                print(f'Failed to assign the scammer role in {guild.name}: {e}')
                                    guildlogchannel = await self.bot.db.fetchval('SELECT logch from serverdata WHERE guild_id = $1', guild.id)
                                    channel = guild.get_channel(guildlogchannel)
                                    if channel is not None:
                                        try:
                                            await channel.send(f'{Configuration.Emoji.caution} **Scammer Alert** {Configuration.Emoji.caution}\n**User : {user.name}**\n**ID:** {user.id}\n**Reason:** {reason}')
                                        except Exception as e:
                                            print(f'{e}')
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Mark Scammer?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a vouchadmin to use this command.')

    @scammer.group(
        name="remove"
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def scammerremove(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to un-mark as scammer.')
            if user == ctx.author:
                return await ctx.error('You cannot un - mark yourself as scammer.')
            data = await self.bot.db.fetchval('SELECT scammer FROM usercheck WHERE user_id = $1', user.id)
            if data is False:
                return await ctx.caution(f'**{user.name}**  as scammer.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , scammer) VALUES ($1 , $2)', user.id, False)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, scammer) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET scammer = EXCLUDED.scammer', user.id, False)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} Scammer Un-Marked.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                            for guild in self.bot.guilds:
                                if user in guild.members:
                                    member = guild.get_member(user.id)
                                    guildscammerrole = await self.bot.db.fetchval('SELECT scammerrole from serverdata WHERE guild_id = $1', guild.id)
                                    role_to_assign = guild.get_role(guildscammerrole)
                                    if role_to_assign:
                                        try:
                                            await member.remove_roles(role_to_assign)
                                        except Exception as e:
                                            print(f'Failed to assign the scammer role in {guild.name}: {e}')
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Un - Mark Scammer?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a vouchadmin to use this command.')
        

    @commands.group(
        invoke_without_command = True,
        name="dwc"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dwc(self, ctx):
        return await ctx.caution('Please Enter a valid argument `[ add / remove ]`')
    

    @dwc.group(
        name="add"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dwcadd(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to mark as Dwc.')
            if user == ctx.author:
                return await ctx.error('You cannot mark yourself as Dwc.')
            data = await self.bot.db.fetchval('SELECT dwc FROM usercheck WHERE user_id = $1', user.id)
            if data is True:
                return await ctx.caution(f'**{user.name}** is marked as scammer.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , dwc) VALUES ($1 , $2)', user.id, True)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, dwc) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET dwc = EXCLUDED.dwc', user.id, True)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} DWC Marked.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                            for guild in self.bot.guilds:
                                if user in guild.members:
                                    member = guild.get_member(user.id)
                                    guilddwcrole = await self.bot.db.fetchval('SELECT dwcrole from serverdata WHERE guild_id = $1', guild.id)
                                    role_to_assign = guild.get_role(guilddwcrole)
                                    if role_to_assign:
                                        try:
                                            await member.add_roles(role_to_assign)
                                        except Exception as e:
                                            print(f'Failed to assign the dwc role in {guild.name}: {e}')
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Mark DWC?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Report Admin to use this command.')
        
    @dwc.group(
        name="remove"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dwcremove(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to un - mark as Dwc.')
            if user == ctx.author:
                return await ctx.error('You cannot mark yourself as Dwc.')
            data = await self.bot.db.fetchval('SELECT dwc FROM usercheck WHERE user_id = $1', user.id)
            if data is False:
                return await ctx.caution(f'**{user.name}** is not marked as dwc.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , dwc) VALUES ($1 , $2)', user.id, False)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, dwc) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET dwc = EXCLUDED.dwc', user.id, False)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} DWC Un - Marked.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                            for guild in self.bot.guilds:
                                if user in guild.members:
                                    member = guild.get_member(user.id)
                                    guilddwcrole = await self.bot.db.fetchval('SELECT dwcrole from serverdata WHERE guild_id = $1', guild.id)
                                    role_to_assign = guild.get_role(guilddwcrole)
                                    if role_to_assign:
                                        try:
                                            await member.remove_roles(role_to_assign)
                                        except Exception as e:
                                            print(f'Failed to assign the dwc role in {guild.name}: {e}')
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Un - Mark DWC?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Repoort Admin to use this command.')



    @commands.group(
        invoke_without_command = True,
        name="blacklist",
        aliases=["bl"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blacklist(self, ctx):
        return await ctx.caution('Please Enter a valid argument `[ add / remove ]`')
    

    @blacklist.group(
        name="add"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bladd(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to blacklist.')
            if user == ctx.author:
                return await ctx.error('You cannot blacklist yourself.')
            data = await self.bot.db.fetchval('SELECT blacklisted FROM usercheck WHERE user_id = $1', user.id)
            if data is True:
                return await ctx.caution(f'**{user.name}** is already Blacklisted.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , blacklisted) VALUES ($1 , $2)', user.id, True)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, blacklisted) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET blacklisted = EXCLUDED.blacklisted', user.id, True)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} Blacklisted.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view=None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Blacklist?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Report Admin to use this command.')
        
    @blacklist.group(
        name="remove"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blremove(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.warn('Please Enter a user to un - blacklist.')
            if user == ctx.author:
                return await ctx.error('You cannot mark yourself as Dwc.')
            data = await self.bot.db.fetchval('SELECT blacklisted FROM usercheck WHERE user_id = $1', user.id)
            if data is False:
                return await ctx.caution(f'**{user.name}** is not blacklisted.')
            else:
                cnfbtn = Button(emoji=f"{Configuration.Emoji.tick}")
                canbtn = Button(emoji=f"{Configuration.Emoji.error}")
                view = View()
                view.add_item(cnfbtn)
                view.add_item(canbtn)
                async def cnfcall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            try:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id , blacklisted) VALUES ($1 , $2)', user.id, False)
                            except:
                                await self.bot.db.execute('INSERT INTO usercheck (user_id, blacklisted) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET blacklisted = EXCLUDED.blacklisted', user.id, False)
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.success,
                                    title=f"{Configuration.Emoji.tick} Un - Blacklisted.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view = None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                async def cancall(interaction: discord.Interaction):
                    if interaction.user == ctx.author:
                        if interaction.user == ctx.author:
                            await interaction.response.edit_message(
                                embed=discord.Embed(
                                    color=Configuration.Colors.error,
                                    title=f"{Configuration.Emoji.error} Command Cancelled.",
                                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                                ),
                                view = None
                            )
                    else:
                        await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.", ephemeral=True)
                cnfbtn.callback = cnfcall
                canbtn.callback = cancall
                e = discord.Embed(
                    color=Configuration.Colors.warn,
                    title=f"{Configuration.Emoji.caution} Un Blacklist?",
                    description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
                await ctx.send(embed=e, view=view)
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Report Admin to use this command.')

    @commands.command(
        name="import",
        aliases=["add"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def import_vouch(self, ctx, user: discord.User = None, amount : int = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.error('Please Enter a user to import the vouches')
            if amount is None:
                return await ctx.warn('Please Enter the amount of vouches to import.')

            else:
                olddata = await self.bot.db.fetchval('SELECT vouches from usercheck WHERE user_id = $1', user.id)
                if not olddata:
                    newdata = amount
                else:
                    newdata = olddata + amount
                try:
                    await self.bot.db.execute('INSERT INTO usercheck (user_id , imported) VALUES ($1 , $2)', user.id, newdata)
                except:
                    await self.bot.db.execute('INSERT INTO usercheck (user_id, imported) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET imported = EXCLUDED.imported', user.id, newdata)
                await ctx.success(f'Successfully imported **{amount}** vouches to **{user.name}**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Report Admin to use this command.')

    @commands.command(
        name="reset",
        aliases=["remove"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reset_vouch(self, ctx, user: discord.User = None):
        allowed = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', ctx.author.id)
        if allowed is True:
            if user is None:
                return await ctx.error('Please Enter a user to reset the vouches')
            else:
                try:
                    await self.bot.db.execute('INSERT INTO usercheck (user_id, imported) VALUES ($1, $2)', user.id, 0)
                except:
                    await self.bot.db.execute('INSERT INTO usercheck (user_id, imported) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET imported = EXCLUDED.imported', user.id, 0)
                await ctx.success(f'Successfully Reset vouches for **{user.name}**')
        else:
            return await ctx.error('Command Invokes.\n >>> Server Not listed in allowed Commands\nYou must be a Report Admin to use this command.')


async def setup(bot):
    await bot.add_cog(AdminCmds(bot))