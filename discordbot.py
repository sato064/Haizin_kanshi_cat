from discord.ext import commands
from os import getenv
import traceback
import discord

bot = commands.Bot(command_prefix='/')
client = discord.Client()

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@client.event
async def on_vc_state_update(menber , before ,after):
    if before.channel != after.channel:
        botRoom = client.get_channel(713740989642178573)
        announceChs = [713740989642178574,918717105136873492]

        if before.channel is not None and before.channel.id in announceChs:
            await botRoom.send("**" + before.channel.name + "** から、__" + menber.name + "__  が抜けました！")
        if after.channel is not None and after.channel.id in announceChs:
            await botRoom.send("**" + after.channel.name + "** に、__" + menber.name + "__  が参加しました！")



token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
client.run(token)
