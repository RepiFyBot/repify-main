import discord
import os 
import sys

def restart_program():
  python = sys.executable
  os.execl(python, python, *sys.argv)

class Configuration():
    token = ""
    owner_ids = [1151502339476312086]

    class Colors:
       default = 0xFDED00
       success = 0xa9ff83
       warn = 0xfeff83
       error = 0xff8385

    class Emoji:
       tick = "<:success:1180159380348469329>"
       error = "<:error:1180159425776975942>"
       warn = "<:warning:1180159488209195049>"
       caution = "<:caution:1180159540411510885>"

    class Database:
      host = ''
      user = ''
      password = ''
      database = ''
      port = 
