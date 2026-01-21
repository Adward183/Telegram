import pandas as pd
import os
from utils.reportSchedule import scheduleReport
from utils.reportTopics import topicsReport
from utils.reportStudents import generateStudentsReport
from utils.reportAttendanceTeachers import attendanceTeachersReport
from utils.reportHomeworkStudents import homeworkStudentsReport
from utils.reportHomeworkTeachers import homeworkTeachersReport

def processExcelFileWithType(file_path, filename, file_type):
    if os.path.getsize(file_path) > 30 * 1024 * 1024:
        return "Файл слишком большой."

    try:
        df = pd.read_excel(file_path, header=[0, 1])
        df.columns = [' '.join(filter(None, map(str, col))).strip() for col in df.columns.values]
    except:
        df = pd.read_excel(file_path)

    if df.empty:
        return "Файл пустой."

    df.columns = [str(col) for col in df.columns]

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