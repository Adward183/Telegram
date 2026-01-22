import os
import sqlite3
from config import MimeTypes, Temp, DB_FILE
from utils.excelProcessor import processExcelFileWithType
from utils.helpers import sendReport
from handlers.commands import user_states, show_main_menu


def register_handlers(bot):  # Обработка документа

    @bot.message_handler(content_types=['document'])
    def handle_document(message):  # Проверка на выбор отчета
        user_id = message.chat.id

        if user_id not in user_states:  # Если не выбрали тип
            show_main_menu(bot, user_id, "Сначала выберите тип отчета:")
            return

        if message.document.mime_type not in MimeTypes:  # Если не соответствует расширению
            bot.send_message(user_id, "Пожалуйста, отправьте файл в формате .xls или .xlsx")
            return

        file_info = bot.get_file(message.document.file_id)  # Получает информацию о файле
        downloaded_file = bot.download_file(file_info.file_path)  # Скачивает файл с серверов
        filename = message.document.file_name  # Формируем имя файла

        temp_path = os.path.join(Temp, f"temp_{user_id}_{filename}")  # Создаем путь для сохранения

        with open(temp_path, 'wb') as new_file:  # Открывает файл для записи
            new_file.write(downloaded_file)

        report_type = user_states[user_id]  # Получаем тип отчета из состояния пользователя
        bot.send_message(user_id, "Обрабатываю файл...")

        response = processExcelFileWithType(temp_path, filename, report_type)
        sendReport(bot, user_id, response)  # Отправляем результат

        # Сохраняем в базу данных
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET report_count = report_count + 1 WHERE user_id = ?",
            (user_id,)
        )

        cursor.execute(
            "INSERT INTO reports (user_id, report_type, filename) VALUES (?, ?, ?)",
            (user_id, report_type, filename)
        )

        conn.commit()
        conn.close()

        bot.send_message(user_id, "Отчет сохранен в статистике")

        if user_id in user_states:
            del user_states[user_id]

        bot.send_message(user_id, "Обработка завершена!")
        show_main_menu(bot, user_id, "Выберите следующий тип отчета:")

        if os.path.exists(temp_path):
            os.remove(temp_path)  # Чистим директорию временных файлов