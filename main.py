import discord
import os
import jishaku
from discord.ui import Button, View
from discord.ext import commands
from core.config import *
from core.repify import Bot



intents = discord.Intents.all()
intents.presences = False
    
bot = Bot (
    intents = intents,
    command_prefix = '+',
    case_insensative = True,
    owner_ids = Configuration.owner_ids,
    activity = discord.Activity(
        status = discord.Status.dnd,
        type = discord.ActivityType.listening,
        name = '+help | .gg/repify'
    ),
    allowed_mentions = discord.AllowedMentions(
        everyone= False,
        roles = False,
        replied_user = False
    )
)
bot.remove_command('help')






os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"


@bot.event
async def on_ready():
    try:
        await bot.load_extension('jishaku')
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                await bot.load_extension(f"cogs.{name}")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    print(f"-----\nLogged in as: {bot.user} : {bot.user.id}\n-----")

bot.run(Configuration.token, reconnect=True)