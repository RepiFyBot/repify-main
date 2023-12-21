import discord
import re
from discord.ui import Button, View
import typing
from discord.ext import commands
from core.config import *

def clrcheck(colorcode):
    try:
        color = discord.Color(int(colorcode, 16))
        return True
    except ValueError:
        return False

def validurl(url):
    url_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    return url_pattern.match(url)



class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_group(
        name="shop",
        aliases=["store"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, ctx):
        e = discord.Embed(
            color=Configuration.Colors.default,
            title="Shop Commands",
            description="**+shop set** - `Adds Shop Link to your profile.`\n**+shop color** - `Adds custom color to your shop.`\n**+shop forum** - `adds custom forum to your shop.`\n**+shop image** - `Adds a custom image to your shop.`\n**+product set** - `adds products to your shop.`\n**+shop test** - `Show's the sample of your shop.`\n**+shop reset** - `Reset's your shop configuration.`"
        )
        await ctx.send(embed=e)

    @shop.group(
        name="set"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _shopset(self, ctx, vanity= None):
        await ctx.typing()
        if vanity is None:
            embed = discord.Embed(color=Configuration.Colors.warn)
            embed.set_author(name="Commands : Shop")
            embed.add_field(name="Shop Set", value="**Command :**\n```+shop set {vanity}```\n**Example :**\n```+shop set repify```", inline=False)
            embed.set_image(url="https://media.discordapp.net/attachments/1142888433988153365/1142890163425517638/image.png?width=333&height=249")
            return await ctx.send(embed=embed)
        else:
            try:
                await self.bot.db.execute('INSERT INTO shop (user_id, shop) VALUES ($1, $2)', ctx.author.id, vanity)
            except:
                await self.bot.db.execute('INSERT INTO shop (user_id, shop) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET shop = EXCLUDED.shop', ctx.author.id, vanity)
            await ctx.success(f'Shop Link set to https://discord.gg/{vanity}')

    @shop.group(
        name="image"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _shopimg(self, ctx, imgurl = None):
        if imgurl is None:
            return await ctx.error('**Please Enter a URL to set your shop image.**')
        if not validurl(imgurl):
            return await ctx.warn("**Please Enter a valid URL.**")
        else:
            try:
                await self.bot.db.execute('INSERT INTO shop (user_id, img) VALUES ($1, $2)', ctx.author.id, imgurl)
            except:
                await self.bot.db.execute('INSERT INTO shop (user_id, img) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET img = EXCLUDED.img', ctx.author.id, imgurl)
            e = discord.Embed(
                color=Configuration.Colors.success,
                description=f"<:success:1159896689239400549> {ctx.author.mention} : Sucessfully Updated the image for your shop."
            )
            e.set_image(url=imgurl)
            await ctx.send(embed=e)

    @shop.group(
        name="color"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _shopcolor(self, ctx, colorcode: str= None):
        if colorcode is None:
            embed = discord.Embed(color=0x2d3136)
            embed.set_author(name="Commands : Shop")
            embed.add_field(name="Shop Color", value="**Command :**\n```+shop color {color}```\n**Example :**\n```+shop set 2f3136```", inline=False)
            embed.set_image(url="https://media.discordapp.net/attachments/1135232780285005907/1143597131672858706/image.png?width=213&height=184")
            return await ctx.send(embed=embed)
        if not clrcheck(colorcode):
            return await ctx.error("**Please Enter a valid color code.**")
        else:
            try:
                await self.bot.db.execute('INSERT INTO shop (user_id, color) VALUES ($1, $2)', ctx.author.id, colorcode)
            except:
                await self.bot.db.execute('INSERT INTO shop (user_id, color) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET color = EXCLUDED.color', ctx.author.id, colorcode)
            e = discord.Embed(
                color=discord.Color(int(colorcode, 16)),
                description=f"**Successfully set your Shop's color to `{colorcode}`**"
            )
            await ctx.send(embed=e)
        
    
    @shop.group(
        name="forum"
    )
    async def _shopforum(self, ctx, *, forum : str = None):
        if forum is None:
            return await ctx.error('forum message cannot be empty.')
        else:
            try:
                await self.bot.db.execute('INSERT INTO shop (user_id, forum) VALUES ($1 , $2)', ctx.author.id, forum)
            except:
                await self.bot.db.execute('INSERT INTO shop (user_id, forum) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET forum = EXCLUDED.forum', ctx.author.id, forum)
            await ctx.success(f'Sucessfully updated your forum to `{forum}`')

    
    @shop.group(
            name="reset"
    )
    async def _shopreset(self, ctx):
        data = await self.bot.db.fetchval('SELECT shop FROM shop WHERE user_id = $1', ctx.author.id)
        if not data:
            return await ctx.warn('You don\'t have your shop set yet.')
        if data:
            await self.bot.db.execute('DELETE FROM shop WHERE user_id = $1', ctx.author.id)
            await ctx.success('Successfully Restored your Shop Configurations.')

    @shop.group(
            name="test",
    )
    async def _shoptest(self, ctx):
        data = await self.bot.db.fetchval('SELECT shop FROM shop WHERE user_id = $1', ctx.author.id)
        if not data:
            await ctx.error('**You have no shop setup yet.** Use `+shop` to setup your shop.')
        if data:
            shopcolor = await self.bot.db.fetchval('SELECT color from shop WHERE user_id = $1', ctx.author.id)
            shoplink = await self.bot.db.fetchval('SELECT shop from shop WHERE user_id = $1', ctx.author.id)
            shopimg = await self.bot.db.fetchval('SELECT img from shop WHERE user_id = $1', ctx.author.id)
            shopforum = await self.bot.db.fetchval('SELECT forum from shop WHERE user_id = $1', ctx.author.id)
            shopproducts = await self.bot.db.fetchval('SELECT product from shop WHERE user_id = $1', ctx.author.id)
            e = discord.Embed(
                color=discord.Color(int(shopcolor, 16)),
                description="This is only a overview of your shop."
                )
            try:
                if not shopimg:
                    pass
                else:
                    e.set_image(url=f"{shopimg}")
            except:
                pass
            try:
                if not shoplink:
                    e.add_field(name="Shop", value=f"Set This!", inline=False)
                else:
                    e.add_field(name="Shop", value=f"Link : https://discord.gg/{shoplink}", inline=False)
            except:
                pass
            try:
                if not shopforum:
                    e.add_field(name="Forum", value="Set This!", inline=False)
                else:
                    e.add_field(name="Forum", value=f"{shopforum}", inline=False)
            except:
                pass
            try:
                if not shopproducts:
                    e.add_field(name="Products", value="Set This!", inline=False)
                else:
                    e.add_field(name="Products", value=f"{shopproducts}", inline=False)
            except:
                pass
            await ctx.send(embed=e)



    @commands.hybrid_group(
        name="product"
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def product(self, ctx):
        async def product(self, ctx):
            await ctx.error('Please Enter an argument. [add/remove]')

    @product.group(
        name="set"
    )
    async def _productadd(self, ctx, *, product: str = None):
        if product is None:
            return await ctx.warn('Keyword Product is Missing : **Please Enter a product to add**')
        else:
            try:
                await self.bot.execute('INSERT INTO shop (user_id, product) VALUES ($1 , $2)', ctx.author.id, product)
            except:
                await self.bot.db.execute('INSERT INTO shop (user_id, product) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET product = EXCLUDED.product', ctx.author.id, product)
            await ctx.success(f'Added `{product}` in your profile.')



async def setup(bot):
    await bot.add_cog(Shop(bot))