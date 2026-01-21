from telebot import types

user_states = {} #Хранит состояние пользователя: user_id и report_type

REPORT_TYPES = {
    'schedule': "Расписание",
    'topics': "Темы уроков",
    'students_grades': "Оценки студентов",
    'attendance_teachers': "Посещаемость преподавателей",
    'homework_teachers': "ДЗ преподавателей",
    'homework_students': "ДЗ студентов"
} #Словарь типов отчетов и их названий

def show_main_menu(bot, chat_id, message_text=None):
    keyboard = types.InlineKeyboardMarkup(row_width=2) #Создаем inline клавиатуру

    buttons = [] #Массив кнопок
    for key, name in REPORT_TYPES.items(): #Циклом проходимся по словарю и добавляем в массив кнопок
        buttons.append(types.InlineKeyboardButton(name, callback_data=f"type_{key}"))

    keyboard.add(*buttons) #Добавляем в клавиатуру кнопки

    text = message_text or "Выберите тип отчета, который хотите получить:"
    return bot.send_message(chat_id, text, reply_markup=keyboard) #Выводим клавиатуру


def register_handlers(bot): #Обработчик команд
    @bot.message_handler(commands=['start']) #Команда start - приветствие и выбор отчета
    def start(message):
        name = message.from_user.first_name
        show_main_menu(bot, message.chat.id, f"Привет, {name}! Выберите тип отчета:")

    @bot.message_handler(commands=['cancel']) #Команда cancel - отменяем выбор отчета
    def cancel_command(message):
        chat_id = message.chat.id
        if chat_id in user_states:
            del user_states[chat_id]
        show_main_menu(bot, chat_id, "Текущее действие отменено. Выберите тип отчета:")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('type_')) #Обработка нажатия inline кнопок
    def handle_report_type(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)

        report_type = call.data.replace('type_', '')
        user_id = call.message.chat.id
        user_states[user_id] = report_type

        report_name = REPORT_TYPES.get(report_type, report_type)
        bot.answer_callback_query(call.id, f"Выбран тип: {report_name}")

        bot.send_message(
            call.message.chat.id,
            f"Вы выбрали: {report_name}\n"
            f"Теперь загрузите Excel-файл (.xls или .xlsx) с соответствующими данными.\n"
            f"Используйте /cancel для отмены."
        )