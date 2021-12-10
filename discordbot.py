from discord.ext import commands
from os import getenv
import traceback
import discord
import datetime

from discord.ext.commands import bot

# bot = commands.Bot(command_prefix='/')
client = discord.Client()

menbers = ['ぱいん','岳南','すくえあ','SETO','Ka','かりんとぅ','サクレ']
gaknanEnter = datetime.datetime.now

"""
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    logger.info("uoooooooooooooooooooooooo")
    print("oooooooooooooooooooooooo")
    await ctx.send('pong')

"""

@client.event
async def on_voice_state_update(menber , before ,after):
    if before.channel != after.channel:
        botRoom = client.get_channel(713740989642178573)
        announceChs = [713740989642178574,918717105136873492]

        if after.channel is not None and after.channel.id in announceChs:
            print("nuketa")
            if menber.id == 361800927939788802: #gaknan
                global gaknanEnter
                gaknanEnter = datetime.datetime.now
            await botRoom.send("**" + after.channel.name + "** に、__" + menber.name + "__  が参加しました")

        if before.channel is not None and before.channel.id in announceChs:
            print("haitta")
            if menber.id == 361800927939788802: #gaknan
                gaknanLeave = datetime.datetime.now
                gaknanTime = gaknanLeave - gaknanEnter
            await botRoom.send('滞在時間')
            await botRoom.send(gaknanTime)



token = getenv('DISCORD_BOT_TOKEN')
# bot.run(token)
client.run(token)
