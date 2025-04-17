import os
import pandas as pd
import pymorphy2
import re
from collections import Counter
from tqdm import tqdm

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "author_a.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "author_a_lemmas.csv")
FREQ_FILE = os.path.join(BASE_DIR, "data", "processed", "author_a_freq.csv")

morph = pymorphy2.MorphAnalyzer()

# Стоп-слова
STOPWORDS = set([
    "быть", "это", "что", "как", "так", "вот", "тут", "там", "и", "но",
    "а", "или", "же", "да", "нет", "он", "она", "они", "мы", "вы", "ты",
    "с", "к", "по", "на", "из", "у", "от", "про", "для", "без", "за", "до",
    "в", "о", "об", "его", "её", "их", "наш", "ваш", "мой", "твой", "меня",
    "тебя", "тебе", "мне", "них", "нас", "вам", "тому", "него", "неё"
])

def clean_and_lemmatize(text):
    words = re.findall(r"\b[а-яёА-ЯЁ]{2,}\b", str(text).lower())
    lemmas = []
    for word in words:
        parsed = morph.parse(word)[0]
        lemma = parsed.normal_form
        pos = parsed.tag.POS
        if pos in {"NOUN", "VERB", "ADJF", "ADJS"} and lemma not in STOPWORDS:
            lemmas.append(lemma)
    return lemmas

def main():
    df = pd.read_csv(INPUT_FILE)
    all_lemmas = []

    print("Лемматизация сообщений author_a...")

    tqdm.pandas(desc="Обработка сообщений")
    df["lemmas"] = df["text"].progress_apply(clean_and_lemmatize)

    for lemmas in df["lemmas"]:
        all_lemmas.extend(lemmas)

    freq = Counter(all_lemmas)
    freq_df = pd.DataFrame(freq.items(), columns=["lemma", "count"]).sort_values(by="count", ascending=False)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    freq_df.to_csv(FREQ_FILE, index=False, encoding="utf-8")

    print(f"Лемматизация завершена. Сохранено в:\n{OUTPUT_FILE}\n{FREQ_FILE}")
    print(f"Уникальных лемм: {len(freq_df)}")

if __name__ == "__main__":
    main()
