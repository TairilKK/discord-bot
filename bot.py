import discord

import events as e
import commands as c

from discord.ext import commands
from threading import Thread
from flask_app import run_flask
from utils import TOKEN


def setup():
  intents = discord.Intents.default()
  intents.message_content = True
  bot = commands.Bot(command_prefix='!', intents=intents)

  e.setup(bot=bot)
  c.setup(bot=bot)

  t = Thread(target=run_flask)
  t.start()

  bot.run(TOKEN)
  
  return bot, t


