import telebot #Telegram Bot Api
from handlers import commands, documents, messages
from config import Token
from db import init_database  # Импортируем инициализацию

print("~Инициализация базы данных~")
init_database()

bot = telebot.TeleBot(Token, parse_mode=None) #Создаем экземпляр бота

#Регистрация обработчиков
commands.register_handlers(bot)
documents.register_handlers(bot)
messages.register_handlers(bot)

print("~Бот запущен~")
bot.polling(none_stop=True) #Запуск
