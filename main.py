import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "parse_messages.py")

os.makedirs(LOG_DIR, exist_ok=True)

# Лог
log_path = os.path.join(LOG_DIR, f"main_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
log_file = open(log_path, "w", encoding="utf-8")

def log(message):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    console_msg = f"{timestamp} {message}"
    plain_msg = console_msg.replace(Fore.YELLOW, "").replace(Fore.GREEN, "").replace(Fore.RED, "").replace(Fore.CYAN, "").replace(Fore.MAGENTA, "").replace(Style.BRIGHT, "").replace(Style.RESET_ALL, "")
    print(console_msg)
    log_file.write(plain_msg + "\n")

# Проверка .gitkeep
def ensure_gitkeep():
    for p in Path(BASE_DIR).rglob("*"):
        if p.is_dir() and ".git" not in str(p):
            contents = list(p.iterdir())
            gitkeep = p / ".gitkeep"
            if not contents:
                gitkeep.touch(exist_ok=True)
            elif gitkeep.exists() and len(contents) > 1:
                gitkeep.unlink()

ensure_gitkeep()

# Запуск парсера
log(Fore.CYAN + Style.BRIGHT + f"=== Запуск парсера VK HTML ===\n")
log(Fore.YELLOW + f"Запуск: {SCRIPT_PATH}")

process = subprocess.Popen(
    [sys.executable, SCRIPT_PATH],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1
)

for line in process.stdout:
    print(line, end="")
    log_file.write(line)

process.wait()

if process.returncode == 0:
    log(Fore.GREEN + f"✅ Завершено успешно")
else:
    log(Fore.RED + f"❌ Ошибка при выполнении скрипта")

log_file.close()
