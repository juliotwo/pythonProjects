TOKEN="1739128825:AAGXh6zm0Ra3yvE9b7mQ0JhKavHoVbxsrqs"

import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start","ayuda","help"])


def cmd_start(message):
    bot.reply_to(message,"hola como andas")

@bot.message_handler(content_types=["text"])

def bot_messages_text(message):
    print("message.chat.id")
    print(message.chat.id)
    if message.text.startswith("/"):
        bot.send_message(message.chat.id,"no disponible")
    else:
        bot.send_message(message.chat.id,"Suscribete")
def send_message(message):
    id_chat=1341751041
    bot.send_message(id_chat,message)

if __name__ =="__main__":
    print("INICIANDO")
    bot.infinity_polling()

