# Threadwalker

A modular pipeline for semantic and emotional analysis of VK message archives. Fully automated, open-source.

---

**Threadwalker** is an open-source tool for parsing and analyzing message threads exported from VKontakte (VK) in HTML format.

This project is under active development. The current version focuses on **parsing raw VK HTML exports into a clean, unified CSV format**.

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

Parsed results will be saved as a CSV file:

```
data/processed/messages.csv
```

With the following fields:
- `dialog_id`: folder name representing the conversation
- `sender`: name of the message author
- `datetime`: message timestamp (ISO 8601)
- `text`: message body (or `[attachment]` if missing)

---

## 🚀 Usage

To parse all HTML files:

```bash
python scripts/parse_messages.py
```

Make sure all dependencies are installed.

---

## 📦 Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```

Main packages:
- `beautifulsoup4`
- `pandas`
- `tqdm`
- `chardet`

---

## 📁 Project Structure

```
Threadwalker/
├── data/
│   ├── raw/           # Raw VK HTML exports (nested by dialog_id)
│   └── processed/     # Output CSV
├── scripts/
│   └── parse_messages.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧪 Example Output (CSV)
```csv
dialog_id,sender,datetime,text
123456,John Doe,2023-05-01T13:47:22,Hey! Long time no see.
123456,Me,2023-05-01T13:48:00,Hi! Yeah, how have you been?
```

---

## 📌 Notes

- Russian datetime strings like `19 фев 2022 в 03:42:03` are normalized to ISO format.
- Attachments are marked as `[attachment]` in the `text` field.
- This parser supports **multi-user** and **multi-folder** exports out of the box.

---

## 🛠 License

MIT — free for personal or commercial use.
