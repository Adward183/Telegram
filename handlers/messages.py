from handlers.commands import show_main_menu


def register_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_messages(message):
        text = message.text.lower()

        if text in ['начать', 'start', '/start']:
            name = message.from_user.first_name
            show_main_menu(bot, message.chat.id, f'Привет, {name}! Выберите тип отчета:')
        elif text == 'id':
            bot.reply_to(message, f'Ваш ID: {message.from_user.id}')
        else:
            show_main_menu(bot, message.chat.id, "Выберите тип отчета:")