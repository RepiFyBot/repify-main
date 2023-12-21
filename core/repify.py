import discord
import os
import json
from discord.ext import commands
from core.config import Configuration
import asyncpg



class Context(commands.Context):

    async def success(self, text):
        user = self.author
        await self.reply(embed=discord.Embed(description=f'{Configuration.Emoji.tick} {user.mention}: {text}', color=Configuration.Colors.success), mention_author=False)

    async def warn(self, text):
        user = self.author
        await self.send(embed=discord.Embed(description=f'{Configuration.Emoji.warn} {user.mention}: {text}', color=Configuration.Colors.warn))

    async def caution(self, text):
        user = self.author
        await self.send(embed=discord.Embed(description=f'{Configuration.Emoji.caution} {user.mention}: {text}', color=Configuration.Colors.warn))

    async def error(self, text):
        user = self.author
        await self.send(embed=discord.Embed(description=f'{Configuration.Emoji.error} {user.mention}: {text}', color=Configuration.Colors.error))

class Bot(commands.Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    async def on_connect(self):
      await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=f'+help | .gg/repifybot'))

    async def get_context(self, message, *, cls = Context):
        return await super().get_context(message, cls = cls)
    
    async def setup_hook(self) -> None:
        self.conn = await asyncpg.connect(user='postgres', password='Neon@Gamer3001', host='db.hnqvwzkucnqptnwjkbfs.supabase.co', port=5432, database='postgres')
        self.db = self.conn

        with open("./schemas/database.sql", "r") as f:
            await self.db.execute(f.read())



    async def on_message(self, msg):
        if (
            not self.is_ready()
            or msg.author.bot
            or msg.guild is None
        ):
            return
        await self.process_commands(msg)