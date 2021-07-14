import os
import sys
# from PIL import Image
import redis
import telebot
from telebot import types
from dotenv import load_dotenv
load_dotenv()

stickerDatabase = redis.Redis(host='0.0.0.0', port=int(sys.argv[1]), db=0,charset="utf-8", decode_responses=True)

# initialise bot 
bot = telebot.TeleBot(os.environ['BOT_API_KEY'], parse_mode='MARKDOWN')
owner_id=os.environ['OWNER_ID']
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "InlineStickerBot,\nyou send stickers here to add them to database, find em through tags inline in any chat instantaneously")


@bot.message_handler(commands=['addtags'])
def add_sticker(message):
    if str(message.from_user.id) in stickerDatabase.smembers("authorized"):
        try:
            replied_sticker_id = str(message.json['reply_to_message']['sticker']['file_id'])
            for tags in str(message.text).split(" "):
                stickerDatabase.sadd(replied_sticker_id,tags)
            bot.reply_to(message,f"Added sticker id to database.")
        except KeyError:
            bot.reply_to(message,"I dont see any replied sticker...")
        except Exception as e:
            bot.reply_to(message,e)
    else:
        bot.reply_to(message,"You aren't authorized to contribute stickers.")

@bot.message_handler(commands=['authorize'])
def add_sticker(message):
    try:
        if str(message.from_user.id) == owner_id:
            print(str(message.from_user.id))
            user_id=message.json["reply_to_message"]["from"]["id"]
            print(user_id)
            stickerDatabase.sadd("authorized",user_id)
            bot.reply_to(message,f"Added @{str(message.from_user.username)} to authorized list of users.")
        else:
            bot.reply_to(message,"Only owner can add/remove contributors.")
    except KeyError:
        bot.reply_to(message,"I dont see anyone replied to...")
    except Exception as e:
        bot.reply_to(message,e)

@bot.message_handler(commands=['unauthorize'])
def add_sticker(message):
    try:
        if str(message.from_user.id) == owner_id:
            print(str(message.from_user.id))
            user_id=message.json["reply_to_message"]["from"]["id"]
            print(user_id)
            stickerDatabase.srem("authorized",user_id)
            bot.reply_to(message,f"Removed @{str(message.from_user.username)} from authorized list of users.")
        else:
            bot.reply_to(message,"Only owner can add/remove contributors.")
    except KeyError:
        bot.reply_to(message,"I dont see anyone replied to...")
    except Exception as e:
        bot.reply_to(message,e)


def alwaystrue(message):
    return True


@bot.inline_handler(func=alwaystrue)
def testmessage(inline_query):
    try:
        results=[]
        for index,stickers in enumerate(stickerDatabase.keys()):
            if set(inline_query.query.split(" ")).issubset(stickerDatabase.smembers(stickers)):
                r=types.InlineQueryResultCachedSticker(index,stickers)
                results.append(r)
        bot.answer_inline_query(inline_query.id, results)
    except Exception as e:
        print(e)


bot.polling()