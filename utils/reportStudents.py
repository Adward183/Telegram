import pandas as pd

def generateStudentsReport(df):
    report = "~Отчет по оценкам студентов~\n\n"

    name_col = find_column(df, ['FIO'])
    homework_col = find_column(df, ['Homework'])
    classroom_col = find_column(df, ['Classroom'])

    if not name_col:
        report += "Не найден столбец 'FIO'\n"
        report += f"Доступные столбцы: {list(df.columns)}\n"
        return report

    if not homework_col:
        report += "Не найден столбец 'Homework'\n"
        return report

    if not classroom_col:
        report += "Не найден столбец 'Classroom'\n"
        return report

    problem_students = []
    total_students = 0

    for idx, row in df.iterrows():
        student_name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        if not student_name or student_name.lower() in ['', 'nan', 'none']:
            continue

        total_students += 1

        hw_score = to_number(row[homework_col])
        class_score = to_number(row[classroom_col])

        if hw_score == 1 and class_score < 3:
            problem_students.append({
                'name': student_name,
                'homework': hw_score,
                'classroom': class_score,
                'row': idx + 2
            })

    report += f"Всего студентов найдено: {total_students}\n"
    report += f"С проблемными оценками ( ДЗ = 1 и КР < 3): {len(problem_students)}\n\n"

    if problem_students:
        report += "Студенты с проблемными оценками:\n\n"

        for i, student in enumerate(problem_students, 1):
            report += f"{i}. {student['name']}\n"
            report += f"Домашняя работа: {student['homework']}\n"
            report += f"Классная работа: {student['classroom']}\n"
            report += f"Строка в файле: {student['row']}\n\n"
    else:
        report += "Студентов с проблемными оценками не найдено.\n"

    return report

def find_column(df, possible_names):
    for col in df.columns:
        col_lower = str(col).lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None

def to_number(value):
    if pd.isna(value):
        return 0
    try:
        return int(value)
    except:
        return 0