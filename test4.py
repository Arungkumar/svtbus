import test_key
import telebot


API_KEY = test_key.api_key
bot = telebot.TeleBot(API_KEY)
print(API_KEY)


@bot.message_handler(commands=["test"])
def tomorrow(message):
    if (message.chat.id == 218393491) or (message.chat.id == 1790734989):
        bot.reply_to(message, "Hello User")
    # updates = bot.get_updates()
    print(message.chat.id)


bot.polling()
