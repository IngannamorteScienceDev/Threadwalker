import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

# Пути проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Лог-файл
log_path = os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
log_file = open(log_path, "w", encoding="utf-8")


def log(message):
    """
    Логирует сообщение в консоль и лог-файл.
    """
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    console_msg = f"{timestamp} {message}"
    plain_msg = console_msg
    for color in [Fore.YELLOW, Fore.GREEN, Fore.RED, Fore.CYAN, Fore.MAGENTA, Style.BRIGHT, Style.RESET_ALL]:
        plain_msg = plain_msg.replace(color, "")
    print(console_msg)
    log_file.write(plain_msg + "\n")


def ensure_gitkeep():
    """
    Добавляет .gitkeep в пустые папки и удаляет их, если они больше не нужны.
    """
    for p in Path(BASE_DIR).rglob("*"):
        if p.is_dir() and ".git" not in str(p):
            contents = list(p.iterdir())
            gitkeep = p / ".gitkeep"
            if not contents:
                gitkeep.touch(exist_ok=True)
            elif gitkeep.exists() and len(contents) > 1:
                gitkeep.unlink()


def run_script(script_name):
    """
    Запускает скрипт по имени, логирует результат.
    """
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    log(Fore.CYAN + Style.BRIGHT + f"\n=== Запуск {script_name} ===")

    process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )

    for line in process.stdout:
        print(line, end="")
        log_file.write(line)

    process.wait()
    if process.returncode == 0:
        log(Fore.GREEN + f"✅ Скрипт {script_name} завершён успешно")
    else:
        log(Fore.RED + f"❌ Ошибка при выполнении {script_name}")


def main():
    if sys.platform == "win32":
        os.system("chcp 65001 >nul")  # Переключаем PowerShell в UTF-8

    log(Style.BRIGHT + Fore.YELLOW + "Threadwalker: запуск полного пайплайна")
    ensure_gitkeep()

    # Этапы
    run_script("parse_messages.py")
    run_script("add_author_role.py")
    run_script("split_by_author.py")

    # Лемматизация
    run_script("lemmatize_author_a.py")
    run_script("lemmatize_author_b.py")
    run_script("lemmatize_author_a_advanced.py")
    run_script("lemmatize_author_b_advanced.py")

    log(Fore.MAGENTA + Style.BRIGHT + "\n🎉 Пайплайн завершён")


if __name__ == "__main__":
    main()
