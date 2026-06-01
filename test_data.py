import random
import string
from datetime import datetime


# Данные для успешной регистрации
valid_user = {
    "name": "Алексей Попов",
    "email": "alexey.popov-test@example.com",
    "password": "ValidPass123"
}

# Данные с некорректным паролем (для проверки валидации)
invalid_password_user = {
    "name": "Ольга Новикова",
    "email": "olga.novikova-test@example.com",
    "password": "123"  # Слишком короткий
}

# Пользователь с существующим email 

existing_user = valid_user.copy()


def generate_email(domain: str = "max.com") -> str:
    """
    Генерирует уникальный email на основе случайного имени пользователя и временной метки.

    Args:
        domain (str): Домен для email (по умолчанию "max.com").
    Returns:
        str: Сгенерированный email адрес.
    """
    usernames = ["testuser", "qauser", "autotest", "selenium", "tester", "tes", "maxtest", "mixstes"]
    username = random.choice(usernames)
    # Берём последние 6 цифр от временной метки в миллисекундах для уникальности
    timestamp = str(int(datetime.now().timestamp() * 1000))[-6:]
    email = f"{username}_{timestamp}@{domain}"
    return email

# Данные для успешной регистрации с генерацией нового email
password_user = {
    "name": "Мария Иванова",
    "email": generate_email(),
    "password": "ValidPass123"
}
