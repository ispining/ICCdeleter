import telebot, sqlite3, config
from telebot import types
from config import stage, sub_photo, sub_msg, sub_button, sub_url




#создание БД
db = sqlite3.connect("server.db", check_same_thread=False)
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS channels (
id TEXT,
title TEXT
)""")
db.commit()




bot = telebot.TeleBot("1617990656:AAHt6thVeoIU7IyNRcftTgzBUOATGy_AtmQ", parse_mode=None)

@bot.message_handler(content_types=["new_chat_members", "left_chat_member"])
def new_chat_members(message):
    sql.execute(f'SELECT id FROM channels WHERE id = "{str(message.chat.id)}"')
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channels VALUES(?, ?)", (str(message.chat.id), message.chat.title))
        db.commit()
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == "private":
        msg = '''
למחיקת הודעות הצטרפות - הוסף בוט זה למנהלי הקבוצה.

Add this bot to your group as Admin if you need to delete join messages
        '''
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["sub"])
def sub(message):
    bot.send_message(message.chat.id, "enter admin password:")
    config.stage = "pswd"


@bot.message_handler(content_types="text")
def msg(message):
    if config.stage == 2:
        config.sub_msg = message.text
        config.stage = 3
        msg = "שלח את טקסט הכפתור"
        bot.send_message(message.chat.id, msg)

    elif config.stage == 3:
        config.stage = 4
        config.sub_button = message.text
        msg = "שלח את קישור הכפתור"
        bot.send_message(message.chat.id, msg)

    elif config.stage == 4:
        num = 0
        config.sub_url = message.text
        k = types.InlineKeyboardMarkup()
        k.row(types.InlineKeyboardButton(str(config.sub_button), url=str(config.sub_url)))
        for row in sql.execute(f'SELECT * FROM channels'):
            try:
                bot.send_photo(chat_id=int(row[0]), photo=config.sub_photo, caption=str(config.sub_msg), reply_markup=k)
                num = num +1
            except:
                pass
        bot.send_message(message.chat.id, f"ההודעה נשלחה ל {str(num)} ערוצים")

    elif config.stage == 5:
        config.sub_msg = message.text
        config.stage = 6
        msg = "שלח את טקסט הכפתור"
        bot.send_message(message.chat.id, msg)

    elif config.stage == 6:
        config.stage = 7
        config.sub_button = message.text
        msg = "שלח את קישור הכפתור"
        bot.send_message(message.chat.id, msg)

    elif config.stage == 7:
        num = 0
        config.sub_url = message.text
        k = types.InlineKeyboardMarkup()
        k.row(types.InlineKeyboardButton(str(config.sub_button), url=str(config.sub_url)))
        for row in sql.execute(f'SELECT * FROM channels'):
            try:
                bot.send_message(int(row[0]), str(config.sub_msg), reply_markup=k)
                num = num +1
            except:
                pass
        bot.send_message(message.chat.id, f"ההודעה נשלחה ל {str(num)} ערוצים")

    elif config.stage == "pswd":
        if message.text == "420":
            num = 0
            if message.chat.type == "private":
                for row in sql.execute(f'SELECT * FROM channels'):
                    num = num + 1
                config.stage = None
                config.sub_photo = None
                config.sub_msg = None
                config.sub_button = None
                config.sub_url = None
                k = types.InlineKeyboardMarkup()
                with_photo = types.InlineKeyboardButton("טקסט עם תמונה", callback_data="with_photo")
                only_text = types.InlineKeyboardButton("טקסט ללא תמונה", callback_data="only_text")
                k.row(with_photo)
                k.row(only_text)
                sum = f"*Subscribe channels:* {str(num)}\n\n"
                bot.send_message(message.chat.id, sum + "בחר את האפשרות המתאימה:", reply_markup=k,
                                 parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "wrong password")
            config.stage = None


    else:
        if message.chat.type == "private":
            msg = '''
למחיקת הודעות הצטרפות - הוסף בוט זה למנהלי הקבוצה.

Add this bot to your group as Admin if you need to delete join messages
            '''

            bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types="photo")
def photo(message):
    if config.stage == 1:
        config.sub_photo = message.photo[0].file_id
        config.stage = 2
        msg = "שלח טקסט"
        bot.send_message(message.chat.id, msg)
        print(config.sub_photo)


@bot.callback_query_handler(func=lambda m: True)
def calls(call):
    if call.data == "with_photo":
        config.stage = 1
        msg = "שלח תמונה"
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "only_text":
        config.stage = 5
        msg = "שלח טקסט"
        bot.send_message(call.message.chat.id, msg)




bot.polling(none_stop=True)
