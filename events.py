import discord
from discord.ext.commands import Bot

def setup(bot: Bot) -> None:
  @bot.event
  async def on_ready() -> None:
    print(f'Logged in as {bot.user}')