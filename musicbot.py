import os
import random
import time
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'ODgzNDA4MTk3ODk2MDA3NzMw.YTJf_w._rCUxm_dXG-_1Xj9NMMpZ-sI7a8'
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"

bot = commands.Bot(command_prefix='!')

@bot.command()
async def join(ctx):
    if (ctx.author.voice): # If the person is in a channel
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send('Bot joined')
    else: #But is (s)he isn't in a voice channel
        await ctx.send("You must be in a voice channel first so I can join it.")

@bot.command()
async def leave(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Bot left')
    else: # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join command to make me join")


@bot.command(name='play')
async def play(ctx,arg):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("./music/" + arg)
        player = voice.play(source)
    else:
        await ctx.send("join vc")

@bot.command(name="list")
async def list(ctx):
    files = os.listdir("./music")
    for i in files:
        await ctx.send(i)

@bot.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No AUDIO")

@bot.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("NO AUDIO PAUSED")

@bot.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()
    await ctx.guild.voice_client.disconnect()

@bot.command(name='seek')
async def seek(ctx,arg):
    player = self.get_player(ctx)
    if player.queue.is_empty:
        raise QueueIsEmpty
    if not (match := re.match(TIME_REGEX, arg)):
        raise InvalidTimeString
    if match.group(3):
        secs = (int(match.group(1)) * 60) + (int(match.group(3)))
    else:
        secs = int(match.group(1))
    await player.seek(secs * 1000)
    await ctx.send("Seeked.")

@bot.command(name="restart")
async def restart_command(self, ctx):
    player = self.get_player(ctx)
    if player.queue.is_empty:
        raise QueueIsEmptyawait
    await player.seek(0)
    await ctx.send("Track restarted.")

bot.run(TOKEN)