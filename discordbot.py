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
async def on_voice_state_update(member , before ,after):
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
            cur.execute("select * from users where user_id = %s",(member.id, ))
            rows = cur.fetchall()
            if not rows:
                cur.execute("INSERT INTO users VALUES (%s, %s ,%s ,%s)",(member.id, member.name,"0",member.guild.id ))
                conn.commit()
                print("new user recorded,He/She is " + member.name)
            cur.execute("INSERT INTO user_entertimes VALUES (%s, %s)",(member.id, str(time.time())))
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
            cur.execute("select * from user_entertimes where user_id = %s",(member.id, ))
            rows = cur.fetchall()
            enter_time = rows[0][1]
            print(enter_time)
            cur.execute("select * from users where user_id = %s",(member.id, ))
            staytimerows = cur.fetchall()
            stay_time = staytimerows[0][2]
            delta_stay_time = float(time.time()) - float(enter_time) + float(stay_time)
            cur.execute("UPDATE users SET user_staytime = %s WHERE user_id = %s",(str(delta_stay_time),member.id ))
            cur.execute("DELETE FROM user_entertimes WHERE user_id = %s",(member.id, ))
            conn.commit()
            conn.close()


@client.event
async def on_message(message):
    if message.content.startswith("/nekoWake"):
        await print_time(message.guild.id,message.channel.id)
    if message.content.startswith("/nekoDebug"):
        print(message.guild.id)
        await debug_time(message.guild.id,message.channel.id)

async def print_time(guild_id,mes_ch_id):
    conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
    )
    cur = conn.cursor()
    cur.execute("select * from users WHERE user_guild_id = %s ORDER BY CAST(user_staytime as signed) DESC",(str(guild_id),))
    rows = cur.fetchall()
    mess = "前回からのサーバ滞在時間報告です．\n"
    count = 1
    for row in rows:
        conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
        )
        cur = conn.cursor()
        stay_sec = round(float(row[2]))
        stay_hours = stay_sec // 3600
        stay_mins = (stay_sec - stay_hours * 3600) // 60
        stay_sec = stay_sec - stay_hours * 3600 - stay_mins * 60 
        this_mess = ("第" + str(count) + "位は " + row[1] + " さん．滞在時間は" + str(stay_hours) + "時間" + str(stay_mins) + "分" + str(stay_sec) + "秒でした．\n") 
        mess += this_mess
        count += 1
        cur.execute("UPDATE users SET user_staytime = %s WHERE user_id = %s",("0",row[0] ))
        conn.commit()
        conn.close()
    print(mess)
    bot_room = client.get_channel(mes_ch_id)
    await bot_room.send(mess)

async def debug_time(guild_id,mes_ch_id):
    conn = mysql.connector.connect(
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASS,
                database = DB_NAME
    )
    cur = conn.cursor()
    cur.execute("select * from users WHERE user_guild_id = %s ORDER BY CAST(user_staytime as signed) DESC",(str(guild_id),))
    rows = cur.fetchall()
    conn.close()
    mess = "前回からのサーバ滞在時間報告です．\n"
    count = 1
    for row in rows:
        stay_sec = round(float(row[2]))
        stay_hours = stay_sec // 3600
        stay_mins = (stay_sec - stay_hours * 3600) // 60
        stay_sec = stay_sec - stay_hours * 3600 - stay_mins * 60 
        this_mess = ("第" + str(count) + "位は " + row[1] + " さん．滞在時間は" + str(stay_hours) + "時間" + str(stay_mins) + "分" + str(stay_sec) + "秒でした．\n") 
        mess += this_mess
        count += 1
    print(mess)
    print(mes_ch_id)
token = getenv('DISCORD_BOT_TOKEN')
# bot.run(token)
client.run(token)
