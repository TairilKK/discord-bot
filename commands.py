import asyncio
import discord
import logging

import yt_dlp as youtube_dl

from utils import get_random_song, insert_song

logging.basicConfig(level=logging.INFO)

def setup(bot):
  @bot.command()
  async def join(ctx):
    if not ctx.message.author.voice:
      await ctx.send("You are not connected to a voice channel")
      return
    else:
      channel = ctx.message.author.voice.channel
    await channel.connect()


  @bot.command()
  async def leave(ctx):
    await ctx.guild.voice_client.disconnect()


  @bot.command()
  async def loop(ctx):
    guild = ctx.guild
    voice_client = guild.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    try:
        while True:
          if not voice_client.is_playing():
            YT_LINK = get_random_song()
            url2 = await extract_info_async(YT_LINK, ydl_opts)
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -ar 48000 -b:a 192k'
            }
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **ffmpeg_options))
          await asyncio.sleep(1)
    except Exception as e:
      logging.error(f'Error in loop command: {e}')
      await ctx.send("An error occurred in the loop.")


  async def extract_info_async(link, ydl_opts):
    loop = asyncio.get_event_loop()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
      return info['url']

  @bot.command()
  async def add_song(ctx, youtube_url: str):
    res = insert_song(url=youtube_url)
    if res == 'Incorrect input':
      await ctx.send('Failed to add the song.')
    elif res == 'Must be unique':
      await ctx.send('Song is already on the list.')
    else:
      await ctx.send(f'Song added: {youtube_url}')