from discord.ext import commands
from os import getenv, name
import traceback
import discord
import datetime
import time
import mysql.connector

client = discord.Client()
DB_HOST = "us-cdbr-east-05.cleardb.net"
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_NAME = "heroku_e41d4f624061a51"

@client.event
async def on_voice_state_update(menber , before ,after):
    if before.channel != after.channel:
        announceChs = [586514492481994765,764127010590949406]
        if after.channel is not None and after.channel.id in announceChs:
            conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
            )
            cur = conn.cursor()
            cur.execute("select * from users where user_id = %s",(menber.id, ))
            rows = cur.fetchall()
            if not rows:
                cur.execute("INSERT INTO users VALUES (%s, %s ,%s)",(menber.id, menber.name,"0"))
                conn.commit()
                print("new user recorded,He/She is " + menber.name)
            cur.execute("INSERT INTO user_entertimes VALUES (%s, %s)",(menber.id, str(time.time())))
            conn.commit()
            conn.close()

        if before.channel is not None and before.channel.id in announceChs:
            conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
            )
            cur = conn.cursor()
            cur.execute("select * from user_entertimes where user_id = %s",(menber.id, ))
            rows = cur.fetchall()
            enter_time = rows[0][1]
            print(enter_time)
            cur.execute("select * from users where user_id = %s",(menber.id, ))
            staytimerows = cur.fetchall()
            stay_time = staytimerows[0][1]
            delta_stay_time = float(time.time()) - float(enter_time) + float(stay_time)
            cur.execute("UPDATE users SET user_staytime = %s WHERE user_id = %s",(str(delta_stay_time),menber.id ))
            cur.execute("DELETE FROM user_entertimes WHERE user_id = %s",(menber.id, ))
            conn.commit()
            conn.close()


@client.event
async def on_message(message):
    if message.content.startswith("/nekoWake"):
        await print_time()
    if message.content.startswith("/nekoDebug"):
        await debug_time()

async def print_time():
    conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
    )
    cur = conn.cursor()
    cur.execute("select * from users ORDER BY CAST(user_staytime as signed) DESC")
    rows = cur.fetchall()
    mess = "前回からのサーバ滞在時間報告です．\n"
    count = 1
    for row in rows:
        staySec = round(float(row[2]))
        stayHours = staySec // 3600
        stayMins = (staySec - stayHours * 3600) // 60
        staySec = staySec - stayHours * 3600 - stayMins * 60 
        this_mess = ("第" + str(count) + "位は " + row[0] + " さん．滞在時間は" + str(stayHours) + "時間" + str(stayMins) + "分" + str(staySec) + "秒でした．\n") 
        mess += this_mess
        count += 1
        cur.execute("UPDATE users SET user_staytime = %s WHERE user_id = %s",("0",row[0] ))
        conn.commit()
        conn.close()
    print(mess)
    botRoom = client.get_channel(920744115740766268)
    await botRoom.send(mess)

async def debug_time():
    conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
    )
    cur = conn.cursor()
    cur.execute("select * from users ORDER BY CAST(user_staytime as signed) DESC")
    rows = cur.fetchall()
    mess = "前回からのサーバ滞在時間報告です．\n"
    count = 1
    for row in rows:
        staySec = round(float(row[2]))
        stayHours = staySec // 3600
        stayMins = (staySec - stayHours * 3600) // 60
        staySec = staySec - stayHours * 3600 - stayMins * 60 
        this_mess = ("第" + str(count) + "位は " + row[0] + " さん．滞在時間は" + str(stayHours) + "時間" + str(stayMins) + "分" + str(staySec) + "秒でした．\n") 
        mess += this_mess
        count += 1
        cur.execute("UPDATE users SET user_staytime = %s WHERE user_id = %s",("0",row[0] ))
        conn.commit()
        conn.close()
    print(mess)
token = getenv('DISCORD_BOT_TOKEN')
# bot.run(token)
client.run(token)
