# Threadwalker

A modular pipeline for semantic and emotional analysis of VK message archives. Fully automated, open-source.

---

**Threadwalker** is an open-source tool for parsing and analyzing message threads exported from VKontakte (VK) in HTML format.

This project is under active development. The current version focuses on:

- Parsing raw VK HTML exports
- Assigning author roles
- Splitting data for individual analysis
- Preparing the data for further semantic and emotional processing

---

## 📥 Input

Place exported VK HTML conversation files inside:

```
data/raw/messages/<dialog_id>/
```

Example:
```
data/raw/messages/123456/
└── messages.html
```

Each `<dialog_id>` should represent a different user or group chat.

---

## 📤 Output

After running the pipeline, you will get:

- `data/processed/messages.csv` — raw parsed messages
- `data/processed/messages_with_roles.csv` — messages with assigned roles
- `data/processed/author_a.csv` — messages by author A
- `data/processed/author_b.csv` — messages by author B
- `data/processed/roles_used.json` — real name mapping to `author_a` / `author_b`

---

## 🚀 Running the Full Pipeline

Just run:

```bash
python main.py
```

This will:

1. Parse all HTML messages
2. Automatically detect the two most frequent senders
3. Assign roles: `author_a`, `author_b`
4. Split messages into separate CSVs
5. Save logs to the `logs/` directory

---

## ⚙️ Custom Role Assignment (Optional)

You can override automatic detection:

### 1. Using CLI arguments:

```bash
python scripts/add_author_role.py --author_a "Name A" --author_b "Name B"
```

### 2. Or via a `config.json` file in the root:

```json
{
  "author_a": "Name A",
  "author_b": "Name B"
}
```

A sample template is included: `config.example.json`

---

## 📦 Installation

Install dependencies via:

```bash
pip install -r requirements.txt
```

Required packages:

- `beautifulsoup4`
- `pandas`
- `tqdm`
- `chardet`
- `colorama`

---

## 📁 Project Structure

```
Threadwalker/
├── data/
│   ├── raw/               # Raw VK HTML exports (nested by dialog_id)
│   └── processed/         # Output CSVs and role metadata
├── scripts/
│   ├── parse_messages.py
│   ├── add_author_role.py
│   └── split_by_author.py
├── logs/                  # Execution logs
│   └── .gitkeep
├── main.py                # Full processing pipeline
├── config.example.json    # Optional config template for role assignment
├── requirements.txt
└── README.md
```

---

## 🧪 Example Output (CSV)

```csv
dialog_id,sender,datetime,text,author_role
123456,Person A,2023-05-01T13:47:22,Hey!,author_a
123456,Person B,2023-05-01T13:48:00,Hi!,author_b
```

---

## 📌 Notes

- Russian datetime strings like `19 фев 2022 в 03:42:03` are normalized to ISO 8601.
- Messages without text (e.g., images, voice messages) are marked as `[attachment]`.
- Parser supports **multi-user**, **multi-folder** exports out of the box.
- All outputs are UTF-8 encoded.

---

## 🛠 License

MIT — free for personal or commercial use.
