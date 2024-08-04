import discord
import sqlite3

import events as e
import commands as c

from discord.ext import commands
from threading import Thread
from flask_app import run_flask
from utils import db_open_connection
from typing import Tuple


def setup(TOKEN: str, SONGS_DB_URL: str) -> Tuple[commands.Bot, Thread, sqlite3.Connection, sqlite3.Cursor]:
  """
  Setup bot.

  Returns:
      List[Bot, Thread]: Bot, Flash server thread
  """  

  song_db_conn, song_curr = db_open_connection(SONGS_DB_URL)

  intents = discord.Intents.default()
  intents.message_content = True
  bot = commands.Bot(command_prefix='!', intents=intents)

  e.setup(bot=bot)
  c.setup(bot=bot)

  t = Thread(target=run_flask)
  t.start()

  bot.run(TOKEN)
  
  return bot, t, song_db_conn, song_curr


