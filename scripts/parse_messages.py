"""
Threadwalker: Парсер HTML-файлов диалогов ВКонтакте
----------------------------------------------------
Этот скрипт извлекает сообщения из экспортированных HTML-файлов ВКонтакте,
поддерживает вложенную структуру папок (одна папка — один диалог),
и сохраняет все сообщения в единый CSV с указанием ID диалога.

Вход:  data/raw/messages/<dialog_id>/*.html
Выход: data/processed/messages.csv
"""

import os
import csv
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import chardet
import datetime

# Определяем корневую директорию проекта относительно местоположения скрипта.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw", "messages")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "messages.csv")

# Словарь для преобразования русских названий месяцев (сокращённо) в номер месяца
month_map = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4,
    "май": 5, "июн": 6, "июл": 7, "авг": 8,
    "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}


def normalize_datetime(datetime_str):
    match = re.search(r"(\d{1,2})\s+([а-яА-Я]+)\s+(\d{4}).*?(\d{1,2}:\d{1,2}:\d{1,2})", datetime_str, re.IGNORECASE)
    if match:
        day, month_str, year, time_str = match.groups()
        try:
            day = int(day)
            year = int(year)
            month_str = month_str.lower()[:3]
            month = month_map.get(month_str)
            if not month:
                return datetime_str
            hour, minute, second = [int(x) for x in time_str.split(":")]
            dt = datetime.datetime(year, month, day, hour, minute, second)
            return dt.isoformat()
        except Exception:
            return datetime_str
    return datetime_str


def decode_file_content(path):
    with open(path, "rb") as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result.get("encoding", "utf-8")
    confidence = result.get("confidence", 0)
    if not encoding or confidence < 0.7:
        encoding = "windows-1251"
    try:
        content = raw_data.decode(encoding)
    except Exception:
        content = raw_data.decode("windows-1251", errors="replace")
    return content


def extract_message_info(html):
    soup = BeautifulSoup(html, "html.parser")
    message_divs = soup.find_all("div", class_="message")
    messages = []

    for msg in message_divs:
        header = msg.find("div", class_="message__header")
        if not header:
            continue

        header_text = header.get_text(" ", strip=True)
        if ',' in header_text:
            parts = header_text.split(',', 1)
            sender = parts[0].strip()
            datetime_raw = parts[1].strip()
        else:
            sender = header_text
            datetime_raw = ""

        datetime_norm = normalize_datetime(datetime_raw) if datetime_raw else ""

        body_divs = msg.find_all("div", recursive=False)
        if len(body_divs) > 1:
            body = " ".join(div.get_text(" ", strip=True) for div in body_divs[1:])
        else:
            body = ""
        if not body:
            body = "[attachment]"

        messages.append({
            "sender": sender,
            "datetime": datetime_norm,
            "text": body
        })
    return messages


def main():
    all_messages = []

    for root, dirs, files in os.walk(RAW_DIR):
        dialog_id = os.path.relpath(root, RAW_DIR).strip(os.sep)
        if dialog_id == ".":
            continue  # Пропускаем саму папку messages/, берём только подпапки
        for filename in sorted(files):
            if not filename.endswith(".html"):
                continue
            path = os.path.join(root, filename)
            html = decode_file_content(path)
            messages = extract_message_info(html)
            for msg in messages:
                msg["dialog_id"] = dialog_id
            all_messages.extend(messages)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["dialog_id", "sender", "datetime", "text"])
        writer.writeheader()
        writer.writerows(all_messages)

    print(f"Parsed {len(all_messages)} messages to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
