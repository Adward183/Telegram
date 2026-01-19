import telebot
from handlers import commands, documents, messages
from config import Token

bot = telebot.TeleBot(Token, parse_mode=None)
commands.register_handlers(bot)
documents.register_handlers(bot)
messages.register_handlers(bot)

print("~Бот запущен~")
bot.polling(none_stop=True)