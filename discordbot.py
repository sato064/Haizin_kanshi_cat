from discord.ext import commands
from os import getenv, name
import traceback
import discord
import datetime
import time
import mysql.connector


from discord.ext.commands import bot

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
                conn.commit()
                print("new user recorded,He/She is " + menber.name)
            else:
                for row in rows:
                    print(row + "Entered room")
                

        if before.channel is not None and before.channel.id in announceChs:
            print(str(menber.name) + "leaved")
            if menber.id == 361800927939788802: #gaknan
                gaknanLeave = time.time()
                gaknanTime = gaknanLeave - gaknanEnter
                global gaknanStayTime
                gaknanStayTime += gaknanTime
                
            if menber.id == 628630250162618378: # Glycine
                glycineLeave = time.time()
                glycineTime = glycineLeave - glycineEnter
                global glycineStayTime
                glycineStayTime += glycineTime

            if menber.id == 408969059657318420: # Ka
                kaLeave = time.time()
                kaTime = kaLeave - kaEnter
                global kaStayTime
                kaStayTime += kaTime
            
            if menber.id == 368770731628036109: # seto
                setoLeave = time.time()
                setoTime = setoLeave - setoEnter
                global setoStayTime
                setoStayTime += setoTime
            
            if menber.id == 402099072733020173: # karintoxu
                kariLeave = time.time()
                kariTime = kariLeave - kariEnter
                global kariStayTime
                kariStayTime += kariTime

            if menber.id == 402099072733020173: # suquare
                suqLeave = time.time()
                suqTime = suqLeave - suqEnter
                global suqStayTime
                suqStayTime += suqTime
            
            if menber.id == 369491047543341057: # sakure
                kosaLeave = time.time()
                kosaTime = kosaLeave - kosaEnter
                global kosaStayTime
                kosaStayTime += kosaTime

            if menber.id == 369834383202320385: # pain
                painLeave = time.time()
                painTime = painLeave - painEnter
                global painStayTime
                painStayTime += painTime

@client.event
async def on_message(message):
    if message.content.startswith("#.ネコ起動"):
        await printTime()

async def printTime():
    global gaknanStayTime,glycineStayTime,kaStayTime,setoStayTime,suqStayTime,painStayTime,kariStayTime,kosaStayTime
    list = [["岳南",round(gaknanStayTime)],["Glycine",round(glycineStayTime)],["Ka",round(kaStayTime)],["SETO",round(setoStayTime)],["かりんとぅ",round(kariStayTime)],["すくえあ",round(suqStayTime)],["5039",round(kosaStayTime)],["ぱいん",round(painStayTime)]]
    botRoom = client.get_channel(586514492481994763)
    list = sorted(list, reverse=True, key=lambda x: x[1])
    print(list)
    count = 1
    mess = "今週の迫真鯖滞在時間を報告します\n"
    for i in list:
        stayDTS = int(i[1])
        stayHour = stayDTS // 3600
        stayTime = (stayDTS - stayHour * 3600) // 60
        staySec = (stayDTS - stayHour * 3600 - stayTime * 60)
        rank = "滞在時間" + str(count) + "位は "+ i[0] + " さん．滞在時間は"+ str(stayHour) +"時間" + str(stayTime) + "分" + str(staySec) + "秒でした．\n"
        mess += rank
        count += 1
    await botRoom.send(mess)
    gaknanStayTime = 0.00
    glycineStayTime = 0.00
    kaStayTime = 0.00
    setoStayTime = 0.00
    painStayTime = 0.00
    suqStayTime = 0.00
    kariStayTime = 0.00
    kosaStayTime= 0.00

token = getenv('DISCORD_BOT_TOKEN')
# bot.run(token)
client.run(token)
