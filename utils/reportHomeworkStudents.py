import pandas as pd


def homeworkStudentsReport(df):
    report = "~Отчет по сданным домашним заданиям студентами~\n\n"

    name_col = find_column(df, ['FIO'])
    percentage_col = find_column(df, ['Percentage Homework', 'Homework Percentage'])

    if not name_col:
        report += "Не найден столбец 'FIO'\n"
        report += f"Доступные столбцы: {list(df.columns)}\n"
        return report

    if not percentage_col:
        report += "Не найден столбец 'Percentage Homework' или 'Homework Percentage'\n"
        return report

    low_performance = []
    total_students = 0

    for idx, row in df.iterrows():
        student_name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        if not student_name or student_name.lower() in ['', 'nan', 'none']:
            continue

        total_students += 1
        percentage_val = row[percentage_col]
        percentage_num = get_percentage(percentage_val)

        if percentage_num is not None and percentage_num < 70:
            low_performance.append({
                'name': student_name,
                'percentage': percentage_num,
                'row': idx + 2
            })

    report += f"Всего студентов: {total_students}\n"
    report += f"С выполнением ДЗ < 70%: {len(low_performance)}\n\n"

    if low_performance:
        report += "Студенты с выполнением ДЗ меньше 70%:\n\n"

        for i, student in enumerate(low_performance, 1):
            report += f"{i}. {student['name']}\n"
            report += f"Выполнение ДЗ: {student['percentage']:.1f}%\n"
            report += f"Строка в файле: {student['row']}\n\n"
    else:
        report += "Все студенты выполняют более 70% ДЗ.\n"

    return report


def find_column(df, possible_names):
    for col in df.columns:
        col_lower = str(col).lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None


def get_percentage(value):
    if pd.isna(value):
        return None
    try:
        num = float(value)
        if 0 <= num <= 1:
            return num * 100
        elif 0 <= num <= 100:
            return num
        return None
    except:
        return None