import pandas as pd


def attendanceTeachersReport(df):
    report = "~Отчет по посещаемости преподавателей~\n\n"

    teacher_col = find_column(df, ['ФИО преподавателя'])
    attendance_col = find_column(df, ['Средняя посещаемость'])

    if not teacher_col:
        report += "Не найден столбец 'ФИО преподавателя'\n"
        report += f"Доступные столбцы: {list(df.columns)}\n"
        return report

    if not attendance_col:
        report += "Не найден столбец 'Посещаемость'\n"
        return report

    low_attendance = []
    total_teachers = 0

    for idx, row in df.iterrows():
        teacher_name = str(row[teacher_col]).strip() if pd.notna(row[teacher_col]) else ""
        if not teacher_name or teacher_name.lower() in ['', 'nan', 'none']:
            continue

        total_teachers += 1
        attendance_val = row[attendance_col]
        attendance_percent = convert_to_percent(attendance_val)

        if attendance_percent is not None and attendance_percent < 40:
            low_attendance.append({
                'teacher': teacher_name,
                'attendance': attendance_percent,
                'row': idx + 2,
                'original_value': attendance_val
            })

    report += f"Всего преподавателей найдено: {total_teachers}\n"

    if low_attendance:
        report += f"С низкой посещаемостью ( меньше 40% ): {len(low_attendance)}\n\n"
        report += "Преподаватели с низкой посещаемостью:\n\n"

        for i, item in enumerate(low_attendance, 1):
            report += f"{i}. {item['teacher']}\n"
            report += f"Посещаемость: {item['attendance']:.1f}%\n"
            report += f"Строка в файле: {item['row']}\n\n"
    else:
        report += "Преподавателей с посещаемостью ниже 40% не найдено.\n"

    return report


def find_column(df, possible_names):
    for col in df.columns:
        col_lower = str(col).lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None


def convert_to_percent(value):
    if pd.isna(value):
        return None

    try:

        if isinstance(value, (int, float)):
            num = float(value)
            if 0 <= num <= 1:
                return num * 100
            elif 0 <= num <= 100:
                return num
            elif num > 100:
                return num
            return None

        value_str = str(value).strip()
        if not value_str or value_str.lower() in ['', 'nan', 'none']:
            return None

        value_str = value_str.replace('%', '').replace(' ', '').replace(',', '.').strip()

        if value_str:
            num = float(value_str)
            if 0 <= num <= 100:
                return num
            elif 0 <= num <= 1:
                return num * 100
            elif num > 100:
                return num
            return None

        return None
    except Exception as e:
        return None