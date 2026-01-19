import os
from config import MimeTypes, Temp
from utils.excelProcessor import processExcelFileWithType
from utils.helpers import sendReport
from handlers.commands import user_states, show_main_menu


def register_handlers(bot):
    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        user_id = message.chat.id

        if user_id not in user_states:
            show_main_menu(bot, user_id, "Сначала выберите тип отчета:")
            return

        if message.document.mime_type not in MimeTypes:
            bot.send_message(user_id, "Пожалуйста, отправьте файл в формате .xls или .xlsx")
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = message.document.file_name

        temp_path = os.path.join(Temp, f"temp_{user_id}_{filename}")

        with open(temp_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        report_type = user_states[user_id]
        bot.send_message(user_id, "Обрабатываю файл...")

        response = processExcelFileWithType(temp_path, filename, report_type)
        sendReport(bot, user_id, response)

        if user_id in user_states:
            del user_states[user_id]

        bot.send_message(user_id, "Обработка завершена!")
        show_main_menu(bot, user_id, "Выберите следующий тип отчета:")

        if os.path.exists(temp_path):
            os.remove(temp_path)