import asyncio
import discord
import logging
import os

import yt_dlp as youtube_dl

from utils import get_random_song_from_directory
from discord.ext.commands import Bot, Context

logging.basicConfig(level=logging.INFO)

def setup(bot: Bot) -> None:
  """
  Adding commands to bot.

  Args:
      bot (Bot): discord bot.
  """  
  @bot.command()
  async def join(ctx: Context) -> None:
    if not ctx.message.author.voice:
      await ctx.send("You are not connected to a voice channel.")
      return
    else:
      channel = ctx.message.author.voice.channel
    await channel.connect()


  @bot.command()
  async def leave(ctx: Context) -> None:
    await ctx.guild.voice_client.disconnect()


  @bot.command()
  async def loop(ctx: Context) -> None:
    guild = ctx.guild
    voice_client = guild.voice_client

    if voice_client is None:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return

    SONGS_DIRECTORY = 'songs'  # Zmień na rzeczywistą ścieżkę do katalogu z plikami mp3

    try:
        while True:
            if not voice_client.is_playing():
                mp3_file = get_random_song_from_directory(SONGS_DIRECTORY)
                voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=mp3_file))
            await asyncio.sleep(1)
    except Exception as e:
        logging.error(f'Error in loop command: {e}')
        await ctx.send("An error occurred in the loop.")
    finally:
        await voice_client.disconnect()
