import os
import pandas as pd
import re
from collections import Counter
from tqdm import tqdm

from razdel import tokenize
from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, Doc
import pymorphy2

# Пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "author_b.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "author_b_lemmas_advanced.csv")
FREQ_FILE = os.path.join(BASE_DIR, "data", "processed", "author_b_freq_advanced.csv")

# NLP-инструменты
segmenter = Segmenter()
embedding = NewsEmbedding()
morph_tagger = NewsMorphTagger(embedding)
backup_morph = pymorphy2.MorphAnalyzer()

# Стоп-слова
STOPWORDS = set([
    "быть", "это", "что", "как", "так", "вот", "тут", "там", "и", "но",
    "а", "или", "же", "да", "нет", "он", "она", "они", "мы", "вы", "ты",
    "с", "к", "по", "на", "из", "у", "от", "про", "для", "без", "за", "до",
    "в", "о", "об", "его", "её", "их", "наш", "ваш", "мой", "твой", "меня",
    "тебя", "тебе", "мне", "них", "нас", "вам", "тому", "него", "неё"
])

def extract_lemmas(text):
    tokens = [t.text for t in tokenize(str(text))]
    lemmas = []

    doc = Doc(" ".join(tokens))
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        lemma = token.lemma
        pos = token.pos

        if not lemma or lemma == token.text:
            parsed = backup_morph.parse(token.text)[0]
            lemma = parsed.normal_form
            pos = parsed.tag.POS

        if pos in {"NOUN", "VERB", "ADJF", "ADJS"} and lemma not in STOPWORDS:
            lemmas.append(lemma)

    return lemmas

def main():
    df = pd.read_csv(INPUT_FILE)
    all_lemmas = []

    tqdm.pandas(desc="Лемматизация author_b")
    df["lemmas"] = df["text"].progress_apply(extract_lemmas)

    for lemmas in df["lemmas"]:
        all_lemmas.extend(lemmas)

    freq = Counter(all_lemmas)
    freq_df = pd.DataFrame(freq.items(), columns=["lemma", "count"]).sort_values(by="count", ascending=False)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    freq_df.to_csv(FREQ_FILE, index=False, encoding="utf-8")

    print(f"Лемматизация завершена: {OUTPUT_FILE}")
    print(f"Частотность сохранена: {FREQ_FILE}")

if __name__ == "__main__":
    main()
