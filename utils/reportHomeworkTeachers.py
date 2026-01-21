import pandas as pd

def homeworkTeachersReport(df):
    report = "~Отчет по проверке домашних заданий преподавателями~\n\n"

    teacher_col = find_column(df, ['ФИО преподавателя'])

    if not teacher_col:
        report += "Не найден столбец 'ФИО преподавателя'\n"
        report += f"Доступные столбцы: {list(df.columns)}\n"
        return report

    month_checked = find_column(df, ['проверено'])
    month_received = find_column(df, ['получено'])
    week_checked = find_column(df, ['проверено'])
    week_received = find_column(df, ['получено'])

    low_checking_month = []
    low_checking_week = []
    total_teachers = 0

    for idx, row in df.iterrows():
        teacher_name = str(row[teacher_col]).strip() if pd.notna(row[teacher_col]) else ""
        if not teacher_name or teacher_name.lower() in ['', 'nan', 'none']:
            continue

        total_teachers += 1

        if month_checked and month_received:
            checked = to_number(row.get(month_checked))
            received = to_number(row.get(month_received))
            if received > 0:
                percentage = (checked / received) * 100
                if percentage < 70:
                    low_checking_month.append({
                        'teacher': teacher_name,
                        'checked': checked,
                        'received': received,
                        'percentage': percentage
                    })

        if week_checked and week_received:
            checked = to_number(row.get(week_checked))
            received = to_number(row.get(week_received))
            if received > 0:
                percentage = (checked / received) * 100
                if percentage < 70:
                    low_checking_week.append({
                        'teacher': teacher_name,
                        'checked': checked,
                        'received': received,
                        'percentage': percentage
                    })

    report += f"Всего преподавателей в файле: {total_teachers}\n\n"

    if low_checking_month:
        report += "Преподаватели с проверкой ДЗ <70% (месяц):\n\n"
        for item in low_checking_month:
            report += f"{item['teacher']}\n"
            report += f"Проверено: {item['checked']:.0f} из {item['received']:.0f}\n"
            report += f"Процент: {item['percentage']:.1f}%\n\n"
    elif month_checked and month_received:
        report += "Все преподаватели проверяют >70% ДЗ за месяц.\n\n"
    else:
        report += "Нет данных для анализа за месяц.\n\n"

    if low_checking_week:
        report += "Преподаватели с проверкой ДЗ <70% (неделя):\n\n"
        for item in low_checking_week:
            report += f"{item['teacher']}\n"
            report += f"Проверено: {item['checked']:.0f} из {item['received']:.0f}\n"
            report += f"Процент: {item['percentage']:.1f}%\n\n"
    elif week_checked and week_received:
        report += "Все преподаватели проверяют >70% ДЗ за неделю.\n\n"
    else:
        report += "Нет данных для анализа за неделю.\n"

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
        return float(value)
    except:
        return 0