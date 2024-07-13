import discord
from discord.ext import commands
from flask import Flask
import yt_dlp as youtube_dl
import asyncio
from random import randint
from utils import TOKEN, get_random_song
from threading import Thread


app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK'

def run_flask():
    app.run(host='0.0.0.0', port=8000)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()
async def play(ctx):
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

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        YT_LINK = get_random_song()
        info = ydl.extract_info(YT_LINK, download=False)
        url2 = info['url']

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -ar 48000 -b:a 192k'
    }

    voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **ffmpeg_options))


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

    while True:
        if not voice_client.is_playing():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                YT_LINK = get_random_song()
                info = ydl.extract_info(YT_LINK, download=False)
                url2 = info['url']
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -ar 48000 -b:a 192k'
            }
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **ffmpeg_options))
        await asyncio.sleep(1)

# Uruchomienie serwera Flask w oddzielnym wątku
t = Thread(target=run_flask)
t.start()
# Uruchomienie bota Discord
bot.run(TOKEN)

