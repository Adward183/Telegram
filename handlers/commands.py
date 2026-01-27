from telebot import types
import sqlite3
from config import DB_FILE, ADMIN_ID

user_states = {}  #Хранит состояние пользователя: user_id и report_type

REPORT_TYPES = {
    'schedule': "Расписание",
    'topics': "Темы уроков",
    'students_grades': "Оценки студентов",
    'attendance_teachers': "Посещаемость преподавателей",
    'homework_teachers': "ДЗ преподавателей",
    'homework_students': "ДЗ студентов"
}  #Словарь типов отчетов и их названий


def show_main_menu(bot, chat_id, message_text=None):
    keyboard = types.InlineKeyboardMarkup(row_width=2)  #Создаем inline клавиатуру

    buttons = []  #Массив кнопок
    for key, name in REPORT_TYPES.items():  #Циклом проходимся по словарю и добавляем в массив кнопок
        buttons.append(types.InlineKeyboardButton(name, callback_data=f"type_{key}"))

    keyboard.add(*buttons)  #Добавляем в клавиатуру кнопки

    text = message_text or "Выберите тип отчета, который хотите получить:"
    return bot.send_message(chat_id, text, reply_markup=keyboard)  # Выводим клавиатуру


def register_handlers(bot):  #Обработчик команд

    @bot.message_handler(commands=['start'])  #Команда start - приветствие и выбор отчета
    def start(message):
        name = message.from_user.first_name
        user_id = message.from_user.id

        # Добавляем пользователя в базу
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (user_id, username, first_name, report_count) VALUES (?, ?, ?, 0)",
                (user_id, message.from_user.username, name)
            )
            print(f"Добавлен пользователь: {name}")

        conn.commit()
        conn.close()

        show_main_menu(bot, message.chat.id, f"Привет, {name}! Выберите тип отчета:")

    @bot.message_handler(commands=['cancel'])  #Команда cancel - отменяем выбор отчета
    def cancel_command(message):
        chat_id = message.chat.id
        if chat_id in user_states:
            del user_states[chat_id]
        show_main_menu(bot, chat_id, "Текущее действие отменено. Выберите тип отчета:")

    @bot.message_handler(commands=['mystats'])  #Команда для статистики пользователя
    def mystats_command(message):
        user_id = message.from_user.id

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT first_name, report_count FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            response = f"Ваша статистика:\n\n"
            response += f"Имя: {row[0]}\n"
            response += f"ID: {user_id}\n"
            response += f"Отчетов создано: {row[1]}\n"
        else:
            response = "Статистика не найдена. Используйте /start для начала работы."

        bot.reply_to(message, response)

    @bot.message_handler(commands=['admin'])  #Админ панель
    def admin_command(message):
        user_id = message.from_user.id

        if user_id not in ADMIN_ID:
            bot.reply_to(message, "У вас нет доступа к админ панели.")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(report_count) FROM users")
        total_reports = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT first_name, report_count FROM users ORDER BY report_count DESC LIMIT 5"
        )
        top_users = cursor.fetchall()

        conn.close()

        response = f"Админ панель\n\n"
        response += f"Всего пользователей: {total_users}\n"
        response += f"Всего отчетов: {total_reports}\n\n"

        if top_users:
            response += "Топ пользователей:\n"
            for i, (name, count) in enumerate(top_users, 1):
                response += f"{i}. {name}: {count} отчетов\n"

        bot.reply_to(message, response)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('type_'))  #Обработка нажатия inline кнопок
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