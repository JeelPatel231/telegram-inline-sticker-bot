import telebot
import os
import database
from telebot import types

bot = telebot.TeleBot(os.environ["BOT_TOKEN"], parse_mode=None)
owner_id=os.environ['OWNER_ID']

method_map = {
    "sticker" : types.InlineQueryResultCachedSticker,
    "animation" : types.InlineQueryResultCachedGif
}

def is_owner(id:str) -> bool:
    return id == owner_id

def check_conditions_met(message,check_reply:bool = True,force_auth:bool=True,force_tags:bool = True) -> bool:
    if check_reply and not message.reply_to_message:
        bot.reply_to(message,"Reply to a Media/Message")
        return False
    
    if force_auth and not (is_owner(str(message.from_user.id)) or database.is_authorised(str(message.from_user.id))):
        bot.reply_to(message,"Not Authorised to contribute!")
        return False

    if force_tags and len(message.text.split(" ",1)) <= 1:
        bot.reply_to(message,"no tags passed in message")
        return False

    return True

def get_attrs(message,force_tags:bool = True) -> tuple:
    type = message.reply_to_message.content_type
    file_id = eval(f'message.reply_to_message.{type}.file_id')
    file_unique_id = eval(f'message.reply_to_message.{type}.file_unique_id')
    if not force_tags: return (file_id,file_unique_id,type)

    tags = message.text.split(" ",1)[1].split(" ")
    return (file_id,file_unique_id,tags,type)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Shut the fuck up!")

@bot.message_handler(commands=['addtags'])
def add_sticker_tags(message):
    if not check_conditions_met(message): return
    data = get_attrs(message)
    database.add_tag(*data)
    bot.reply_to(message,"added")

@bot.message_handler(commands=['remtags'])
def remove_sticker_tags(message):
    if not check_conditions_met(message): return
    data = get_attrs(message)
    database.remove_tag(*data)
    bot.reply_to(message,"removed")

@bot.message_handler(commands=['delete'])
def delete_sticker(message):
    if not check_conditions_met(message,force_tags=False): return
    data = get_attrs(message,False)
    database.delete_sticker(data[1])
    bot.reply_to(message,"deleted")

@bot.message_handler(regexp="^/authori[sz]e$") # authorise , authorize
def auth(message):
    if not check_conditions_met(message,force_tags=False,force_auth=False): return
    if not is_owner(str(message.from_user.id)):
        bot.reply_to(message,"Only Owner can Auth/DeAuth peoples")
        return
    database.add_authorised(str(message.reply_to_message.from_user.id))
    bot.reply_to(message,f"authorised {message.reply_to_message.from_user.username}")

@bot.message_handler(regexp="^/[du][en]authori[sz]e$") # deauthori(s|z)e, unauthori(s|z)e
def auth(message):
    if not check_conditions_met(message,force_tags=False,force_auth=False): return
    if not is_owner(str(message.from_user.id)):
        bot.reply_to(message,"Only Owner can Auth/DeAuth peoples")
        return
    database.remove_authorised(str(message.reply_to_message.from_user.id))
    bot.reply_to(message,f"deauthorised {message.reply_to_message.from_user.username}")

@bot.message_handler(commands=["gettags","showtags"])
def tags(message):
    if not check_conditions_met(message,force_tags=False,force_auth=False): return
    data = get_attrs(message,force_tags=False)
    response = database.get_tags(data[1])
    if response == [] :
        bot.reply_to(message,"Media not found in DB!")
    else:
        bot.reply_to(message,response)

@bot.inline_handler(func=lambda m: True)
def testmessage(inline_query):
    results=[]
    tags = inline_query.query.split(" ")
    print(tags)
    for index,response in enumerate(database.fetch_sticker(tags)):
        results.append(method_map[response[1]](index,response[0]))
        print(index,response)
    bot.answer_inline_query(inline_query.id, results)


bot.infinity_polling()