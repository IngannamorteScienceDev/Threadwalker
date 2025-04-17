import os
import sys
import json
import argparse
import pandas as pd

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "messages.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "messages_with_roles.csv")
ROLES_USED_FILE = os.path.join(BASE_DIR, "data", "processed", "roles_used.json")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("author_a"), config.get("author_b")
        except json.JSONDecodeError:
            print("Ошибка при чтении config.json")
    return None, None


def parse_args():
    parser = argparse.ArgumentParser(description="Assign roles to message authors")
    parser.add_argument("--author_a", type=str, help="Sender name or keyword for author_a")
    parser.add_argument("--author_b", type=str, help="Sender name or keyword for author_b")
    args = parser.parse_args()

    # Сначала из аргументов
    a, b = args.author_a, args.author_b

    # Если не передано — пробуем config.json
    if not a or not b:
        print("Аргументы не указаны — ищем config.json...")
        a_cfg, b_cfg = load_config()
        a = a or a_cfg
        b = b or b_cfg

    return a, b


def classify_sender(sender: str, a_key: str, b_key: str) -> str:
    sender_lower = sender.lower()
    if a_key.lower() == sender_lower:
        return "author_a"
    elif b_key.lower() == sender_lower:
        return "author_b"
    else:
        return "other"


def auto_detect_roles(df: pd.DataFrame):
    top_senders = df["sender"].value_counts().nlargest(2)
    if len(top_senders) < 2:
        print("Недостаточно разных отправителей для автоматического определения ролей.")
        sys.exit(1)
    author_a, author_b = top_senders.index[0], top_senders.index[1]
    print(f"Автоматически определены роли:")
    print(f"  author_a = {author_a}")
    print(f"  author_b = {author_b}")
    return author_a, author_b


def main():
    df = pd.read_csv(INPUT_FILE)

    author_a, author_b = parse_args()

    if not author_a or not author_b:
        author_a, author_b = auto_detect_roles(df)

    # Назначаем роли
    df["author_role"] = df["sender"].apply(lambda s: classify_sender(s, author_a, author_b))

    print("\nСтатистика по ролям:")
    print(df["author_role"].value_counts())

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    # Сохраняем реальные имена в roles_used.json
    with open(ROLES_USED_FILE, "w", encoding="utf-8") as f:
        json.dump({"author_a": author_a, "author_b": author_b}, f, ensure_ascii=False, indent=2)

    print(f"\nСообщения с ролями сохранены в: {OUTPUT_FILE}")
    print(f"Использованные имена сохранены в: {ROLES_USED_FILE}")


if __name__ == "__main__":
    main()
