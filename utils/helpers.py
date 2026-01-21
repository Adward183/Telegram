import tempfile
import os

def sendReport(bot, chat_id, text): #Отправка результата
    if not text:
        return

    filename = get_filename(text)
    send_as_file(bot, chat_id, text, filename)

def get_filename(text): #Анализирует первую строку отчета
    # Определяет тип отчета по уникальному заголовку
    if text.startswith("~Отчет по темам уроков~"):
        return "темы.txt"
    elif text.startswith("~Отчет по оценкам студентов~"):
        return "оценки.txt"
    elif text.startswith("~Отчет по посещаемости преподавателей~") or text.startswith(
            "~Отчет посещаемости преподавателей~"):
        return "посещаемость_преподавателей.txt"
    elif text.startswith("~Отчет по расписанию~"):
        return "расписание.txt"
    elif text.startswith("~Отчет по проверке домашних заданий преподавателями~"):
        return "проверка_дз.txt"
    elif text.startswith("~Отчет по сданным домашним заданиям студентами~"):
        return "сдача_дз.txt"
    else:
        return "отчет.txt" #Возвращает соответствующее имя файла

def send_as_file(bot, chat_id, text, filename):
    #Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as f:
        f.write(text) #Записываем текст отчета
        temp_path = f.name #Получаем путь к файлу

    try:
        #Открываем файл для чтения и отправляем
        with open(temp_path, 'rb') as file:
            bot.send_document(chat_id, file, visible_file_name=filename)
    except Exception as e:
        #Обработка ошибок отправки
        bot.send_message(chat_id, f"Не удалось отправить файл. Ошибка: {str(e)[:100]}")
    finally:
        #Удаляем временный файл
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass