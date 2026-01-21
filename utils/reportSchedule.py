def scheduleReport(df):
    report = "~Отчет по расписанию~\n\n"

    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    day_columns = []

    for col in df.columns:
        col_lower = str(col).lower()
        for day in days:
            if day in col_lower:
                day_columns.append(col)
                break

    if not day_columns:
        report += "Не найдены столбцы с днями недели\n"
        return report

    all_subjects = {}

    for day_col in day_columns:
        for subject in df[day_col].dropna():
            subject_str = str(subject).strip()
            if subject_str and subject_str.lower() != 'nan':
                all_subjects[subject_str] = all_subjects.get(subject_str, 0) + 1

    if all_subjects:
        total_pairs = 0

        for subject, count in sorted(all_subjects.items(), key=lambda x: x[1], reverse=True):
            report += f"{subject}: {count} пар\n"
            total_pairs += count

        report += f"\nВсего пар за неделю: {total_pairs}"
    else:
        report += "В расписании не найдено предметов."

    return report