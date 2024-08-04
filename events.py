import discord
from discord.ext.commands import Bot

def setup(bot: Bot) -> None:
  """
  Setup bot.

  Args:
      bot (Bot): discord bot
  """  
  @bot.event
  async def on_ready() -> None:
    print(f'Logged in as {bot.user}')
