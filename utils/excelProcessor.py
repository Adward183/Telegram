import pandas as pd
import os
from utils.reportSchedule import scheduleReport
from utils.reportTopics import topicsReport
from utils.reportStudents import generateStudentsReport
from utils.reportAttendanceTeachers import attendanceTeachersReport
from utils.reportHomeworkStudents import homeworkStudentsReport
from utils.reportHomeworkTeachers import homeworkTeachersReport

def processExcelFileWithType(file_path, filename, file_type): #Основная функция для работы с файлами
    if os.path.getsize(file_path) > 30 * 1024 * 1024: #Проверяем размер файла (добавил для оптимизации)
        return "Файл слишком большой."

    try:
        df = pd.read_excel(file_path, header=[0, 1]) #Пробуем читать Excel с двумя строками заголовков
        df.columns = [' '.join(filter(None, map(str, col))).strip() for col in df.columns.values] #Преобразуем индекс в плоскую структуру
    except:
        df = pd.read_excel(file_path) #Если не получилось - читаем с одним заголовком

    if df.empty: #Если файл пустой
        return "Файл пустой."

    #Преобразуем заголовки, они не все могут быть строкой, делается для простоты и удобства
    df.columns = [str(col) for col in df.columns]

    #Тип отчета обрабатывается своей функцией
    if file_type == 'topics':
        return topicsReport(df)
    elif file_type == 'schedule':
        return scheduleReport(df)
    elif file_type == 'students_grades':
        return generateStudentsReport(df)
    elif file_type == 'attendance_teachers':
        return attendanceTeachersReport(df)
    elif file_type == 'homework_teachers':
        return homeworkTeachersReport(df)
    elif file_type == 'homework_students':
        return homeworkStudentsReport(df)
    else:
        return f"Неизвестный тип отчета: {file_type}"