import discord
import os
import sys
import datetime
from discord.ext import commands
from core.config import Configuration
from discord.ui import Button, View


def restart_program():
  python = sys.executable
  os.execl(python, python, *sys.argv)

class RestartBtns(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__()

    @discord.ui.button(emoji=f"{Configuration.Emoji.tick}", style=discord.ButtonStyle.gray, custom_id="yes_button")
    async def _yes(self, interaction:discord.Interaction, button):
        embed = discord.Embed(color={Configuration.Colors.default}, description="**Restarting...**")
        await interaction.response.edit_message(embed=embed, view=None)
        restart_program()

    @discord.ui.button(emoji=f"{Configuration.Emoji.error}", style=discord.ButtonStyle.gray, custom_id="no_button")
    async def _no(self, interaction:discord.Interaction, button):
        embed = discord.Embed(color={Configuration.Colors.default}, description="**The Operation Was Cancelled by the Developer.**")
        await interaction.response.edit_message(embed=embed, view=None)


class OwnerCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="restart")
    @commands.is_owner()
    async def _restart(self, ctx):
        embed = discord.Embed(color=0x313239, description="**Do You Want to restart The bot ?**", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar.url}")
        embed.set_footer(text="owner.py : reset command")
        view = RestartBtns()
        await ctx.send(embed=embed , view=view)


    @commands.group(
        invoke_without_command = True,
        name="staff",
        aliases=["majdoor"]
    )
    @commands.is_owner()
    async def staff(self, ctx):
        return await ctx.caution('Please Enter a valid argument `[ add / remove ]`')
    
    @staff.group(
        name="add"
    )
    @commands.is_owner()
    async def staffadd(self, ctx, user:discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to give staff perms')
        data = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', user.id)
        if data is True:
            return await ctx.caution('This user is already having staff privileges.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchstaff) VALUES ($1, $2)', user.id, True)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchstaff) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET vouchstaff = EXCLUDED.vouchstaff', user.id, True)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Staff Added.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall

            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Staff Add?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)

    
    @staff.group(
        name="remove"
    )
    @commands.is_owner()
    async def staffremove(self, ctx, user:discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to remove staff perms')
        data = await self.bot.db.fetchval('SELECT vouchstaff from staffs WHERE user_id = $1', user.id)
        if data is False:
            return await ctx.caution('This user is not having privileges.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchstaff) VALUES ($1, $2)', user.id, False)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchstaff) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET vouchstaff = EXCLUDED.vouchstaff', user.id, False)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Staff Removed.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall

            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Staff Remove?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)

    @commands.group(
        invoke_without_command = True,
        name="admin"
    )
    @commands.is_owner()
    async def admin(self, ctx):
        return await ctx.caution('Please Enter a valid argument `[ add / remove ]`')
    
    @admin.group(
        name="add"
    )
    @commands.is_owner()
    async def adminadd(self, ctx, user : discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to add admin privileges.')
        data = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', user.id)
        if data is True:
            return await ctx.caution('This user is already having admin privileges.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchadmin) VALUES ($1, $2)', user.id, True)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchadmin) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET vouchadmin = EXCLUDED.vouchadmin', user.id, True)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Admin Added.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Admin Add?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)


    @admin.group(
        name="remove"
    )
    @commands.is_owner()
    async def adminremove(self, ctx, user : discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to add admin privileges.')
        data = await self.bot.db.fetchval('SELECT vouchadmin from staffs WHERE user_id = $1', user.id)
        if data is False:
            return await ctx.caution('This user is not having admin privileges.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchadmin) VALUES ($1, $2)', user.id, False)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, vouchadmin) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET vouchadmin = EXCLUDED.vouchadmin', user.id, False)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Admin Removed.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Admin Remove?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)


    @commands.group(
        invoke_without_command = True,
        name="noprefix",
        aliases=["np"]
    )
    @commands.is_owner()
    async def noprefix(self, ctx):
        return await ctx.caution('Please Enter a user to give noprefix.')
    
    @noprefix.group(
        name="add"
    )
    @commands.is_owner()
    async def npadd(self, ctx, user : discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to give No Prefix.')
        data = await self.bot.db.fetchval('SELECT noprefix from staffs WHERE user_id = $1', user.id)
        if data is True:
            return await ctx.caution('This user is already having No - Prefix.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, noprefix) VALUES ($1, $2)', user.id, True)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, noprefix) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET noprefix = EXCLUDED.noprefix', user.id, True)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Noprefix Added.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Noprefix Add?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)



    @noprefix.group(
        name="remove"
    )
    @commands.is_owner()
    async def npremove(self, ctx, user : discord.User = None):
        if user is None:
            return await ctx.warn('Please Mention a user to remove No Prefix.')
        data = await self.bot.db.fetchval('SELECT noprefix from staffs WHERE user_id = $1', user.id)
        if data is False:
            return await ctx.caution('This user Not a No - Prefix user.')
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
                            await self.bot.db.execute('INSERT INTO staffs (user_id, noprefix) VALUES ($1, $2)', user.id, False)
                        except:
                            await self.bot.db.execute('INSERT INTO staffs (user_id, noprefix) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET noprefix = EXCLUDED.noprefix', user.id, False)
                        await interaction.response.edit_message(
                            embed=discord.Embed(
                                color=Configuration.Colors.success,
                                title=f"{Configuration.Emoji.tick} Noprefix Removed.",
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
                            embed = discord.Embed(
                                color=Configuration.Colors.error,
                                title=f"{Configuration.Emoji.error} Command Cancelled.",
                                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                            ),
                            view=None
                        )
                else:
                    await interaction.response.send_message(f"{Configuration.Emoji.caution} You cannot use this button.")

            cnfbtn.callback = cnfcall
            canbtn.callback = cancall
            e = discord.Embed(
                color=Configuration.Colors.warn,
                title=f"{Configuration.Emoji.caution} Noprefix Remove.?",
                description=f"**Mention:** {user.mention}\n**Username:** {user.name}\n**ID:** {user.id}"
                )
            await ctx.send(embed=e, view=view)


async def setup(bot):
    await bot.add_cog(OwnerCmds(bot))