from discord.ext import commands
from os import getenv, name
import traceback
import discord
import datetime
import time
import mysql.connector

# bot = commands.Bot(command_prefix='/')
client = discord.Client()

# 一時変数
gaknanEnter = time.time()
glycineEnter = time.time()
kaEnter = time.time()
setoEnter = time.time()
kariEnter = time.time()
suqEnter = time.time()
kosaEnter = time.time()
painEnter = time.time()

# 保管変数
gaknanStayTime = 0.00
glycineStayTime = 0.00
kaStayTime = 0.00
setoStayTime = 0.00
kariStayTime = 0.00
suqStayTime = 0.00
kosaStayTime = 0.00
painStayTime = 0.00

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
        announceChs = [586514492481994765,764127010590949406]
        if after.channel is not None and after.channel.id in announceChs:
            conn = mysql.connector.connect(
                host = "us-cdbr-east-05.cleardb.net",
                user = getenv("DB_USER"),
                password = getenv("DB_PASS"),
                database = "heroku_e41d4f624061a51"
            )
            cur = conn.cursor()
            cur.execute("select * from users where user_id = %s",(menber.id, ))
            rows = cur.fetchall()
            if not rows:
                cur.execute("INSERT INTO users VALUES (%s, %s)",(menber.id, menber.name))
                cur.execute("INSERT INTO user_staytimes VALUES (%s, 0)",(menber.name, ))
                conn.commit()
                print("new user recorded,He/She is " + menber.name)
            else:
                for row in rows:
                    print(row)
            cur.execute("INSERT INTO user_entertimes VALUES (%s, %s)",(menber.id, str(time.time())))
            conn.commit()
            conn.close()

        if before.channel is not None and before.channel.id in announceChs:
            conn = mysql.connector.connect(
                host = "us-cdbr-east-05.cleardb.net",
                user = getenv("DB_USER"),
                password = getenv("DB_PASS"),
                database = "heroku_e41d4f624061a51"
            )
            cur = conn.cursor()
            cur.execute("select * from user_entertimes where user_id = %s",(menber.id, ))
            rows = cur.fetchall()
            enter_time = rows[0][1]
            print(enter_time)
            cur.execute("select * from user_staytimes where user_id = %s",(menber.id, ))
            staytimerows = cur.fetchall()
            stay_time = staytimerows[0][1]
            this_stay_time = float(time.time()) - float(enter_time) + float(stay_time)
            cur.execute("UPDATE user_staytimes SET user_stay_time = %s WHERE user_id = %s",(str(this_stay_time),menber.id ))
            cur.execute("DELETE FROM user_entertimes WHERE user_id = %s",(menber.id, ))
            conn.commit()
            conn.close()


@client.event
async def on_message(message):
    if message.content.startswith("#.ネコ起動"):
        await printTime()

async def printTime():
    conn = mysql.connector.connect(
                host = "us-cdbr-east-05.cleardb.net",
                user = getenv("DB_USER"),
                password = getenv("DB_PASS"),
                database = "heroku_e41d4f624061a51"
    )
    cur = conn.cursor()
    cur.execute("select * from user_staytimes ORDER BY CAST(user_stay_time as signed) DESC")
    rows = cur.fetchall()
    for row in rows:
        print(row)

token = getenv('DISCORD_BOT_TOKEN')
# bot.run(token)
client.run(token)
