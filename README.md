# 🧠 Threadwalker

> A modular pipeline for semantic and emotional analysis of VK message archives. Fully automated, open-source.

---

## 📁 Project Structure

```
Threadwalker/
├── data/
│   ├── raw/                    # Original VK HTML files
│   └── processed/              # Parsed and analyzed CSV outputs
├── logs/                       # Execution logs
├── scripts/                    # Analysis, lemmatization and visualization scripts
├── main.py                     # Full pipeline runner
├── config.example.json         # Optional roles configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/IngannamorteScienceDev/Threadwalker.git
cd Threadwalker
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> ℹ️ On Windows, the terminal will automatically switch to UTF-8 (`chcp 65001`) for correct Unicode output.

---

## 🔄 Pipeline Stages

1. **HTML Parsing**  
   → `data/processed/messages.csv`

2. **Automatic Role Assignment**  
   → adds `author_role` column (`author_a`, `author_b`)

3. **Message Splitting**  
   → `author_a.csv`, `author_b.csv`

4. **Lemmatization**
   - `lemmatize_author_a.py`, `lemmatize_author_b.py`: basic using pymorphy2
   - `*_advanced.py`: hybrid Natasha + pymorphy2 fallback

---

## 🧪 Output Examples

| File                             | Description                           |
|----------------------------------|---------------------------------------|
| `messages_with_roles.csv`        | All messages with assigned roles      |
| `author_a_lemmas.csv`            | Lemmatized messages from author A     |
| `author_a_freq.csv`              | Lemma frequency counts                |
| `author_a_lemmas_advanced.csv`   | More accurate lemmatization (Natasha) |

---

## ⚙ Role Configuration (Optional)

You can override automatic role detection using a config file:

```json
{
  "author_a": "You",
  "author_b": "John Doe"
}
```

Place it in the root directory as `config.json`. Use `config.example.json` as a starting point.

---

## 📦 Dependencies

Listed in `requirements.txt`:

```
pymorphy2
natasha
razdel
tqdm
bs4
chardet
colorama
```

---

## 🛠 Roadmap

- [ ] Lovely words analysis
- [ ] Emotion classification (EmoBERT)
- [ ] Topic modeling (BERTopic / LDA)
- [ ] Streamlit-based semantic dashboard
