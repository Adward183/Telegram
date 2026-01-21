import os #Работа с файлами

Token = "8493080910:AAE-LWsPVF8LYoO_ptLB4yMdL_q3P1r5NNo" #Токен бота

MimeTypes = [
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
] #Поддержка типов расширений Exel .xls и .xlsx

Temp = "temp" #Инициализация папки для временных данных

os.makedirs(Temp, exist_ok=True) #Создаем директорию