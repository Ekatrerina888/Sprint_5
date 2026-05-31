import random
import string
import time


# --- Функции генерации ---

def generate_email(domain: str = "max.com") -> str:
    usernames = ["testuser", "qauser", "autotest", "selenium", "tester", "tes", "maxtest", "mixstes"]
    username = random.choice(usernames)
    timestamp = str(int(time.time() * 1000))[-6:]
    email = f"{username}_{timestamp}@{domain}"
    return email

def generate_password(length: int = 8) -> str:
    if length < 6:
        raise ValueError("Пароль должен быть не менее 6 символов")
    characters = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_name() -> str:
    names = ["Анна", "Мария", "Екатерина", "Ольга", "Наталья", "Ирина", "Светлана", "Юлия", "Виктория", "Влад", "Сева", "Роман", "Михаил", "Николай", "Иван"]
    return random.choice(names)

# --- Тестовые данные ---

def get_registration_data() -> dict:
    """Возвращает словарь с готовыми данными для регистрации."""
    return {
        'name': generate_name(),
        'email': generate_email(),
        'password': generate_password()
    }

def get_login_data() -> dict:
    """Возвращает словарь с готовыми данными для входа."""
    return {
        'email': generate_email(),
        'password': generate_password()
    }


import csv
import os

CSV_FILE = "test_credentials.csv" 

def save_credentials_csv(data: dict, filename: str = CSV_FILE):
    """Добавляет учётные данные в CSV‑файл."""
    fieldnames = ['name', 'email', 'password']
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def load_credentials_csv(filename: str = "test_credentials.csv") -> list:
    """Загружает все учётные данные из CSV‑файла как список словарей."""
    # Диагностика: проверяем существование файла
    if not os.path.exists(filename):
        print(f"❌ Файл {filename} не найден!")
        return []

    # Диагностика: проверяем размер файла
    file_size = os.path.getsize(filename)
    if file_size == 0:
        print("❌ Файл найден, но он пуст!")
        return []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            # Диагностика: читаем первые 100 байт для проверки кодировки
            csvfile.seek(0)
            sample = csvfile.read(100)
            if not sample:
                print("❌ Файл пуст или повреждён!")
                return []
            csvfile.seek(0)  # Возвращаем указатель в начало

            reader = csv.DictReader(csvfile)

            # Диагностика: проверяем наличие заголовков
            if not reader.fieldnames:
                print("❌ В файле нет заголовков (name,email,password)!")
                return []

            data = list(reader)

            # Диагностика: проверяем, есть ли данные (не только заголовки)
            if len(data) == 0:
                print("⚠️ Файл содержит только заголовки, но нет данных!")
                return []

            print(f"✅ Загружено {len(data)} пользователей из {filename}")
            return data

    except UnicodeDecodeError:
        print("❌ Ошибка кодировки: файл не в UTF-8!")
        return []
    except Exception as e:
        print(f"❌ Неожиданная ошибка при чтении файла: {e}")
        return []