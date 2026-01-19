import re
import pandas as pd

PatternTopic = r'^Урок\s*№\s*\d+\.\s*Тема:\s*.+$'

def topicsReport(df):
    report = "~Отчет по темам уроков~\n\n"

    topic_col = find_column(df, ['Тема урока'])

    if not topic_col:
        report += "Не найден столбец 'Тема урока'\n"
        report += f"Доступные столбцы: {list(df.columns)}\n"
        return report

    incorrect_topics = []
    total_topics = 0

    for idx, row in df.iterrows():
        if pd.isna(row[topic_col]):
            continue

        topic_str = str(row[topic_col]).strip()
        if not topic_str or topic_str.lower() == 'nan':
            continue

        total_topics += 1

        if not re.match(PatternTopic, topic_str):
            incorrect_topics.append((idx + 2, topic_str))

    report += f"Всего тем в файле: {total_topics}\n"
    report += f"Некорректных тем: {len(incorrect_topics)}\n\n"

    if incorrect_topics:
        report += "Некорректно оформленные темы:\n\n"

        for row_num, topic in incorrect_topics:
            report += f"Строка {row_num}: {topic}\n"
    else:
        report += "Все темы оформлены корректно!\n"

    return report


def find_column(df, possible_names):
    for col in df.columns:
        col_lower = str(col).lower()
        for name in possible_names:
            if name.lower() in col_lower:
                return col
    return None