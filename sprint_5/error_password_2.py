from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random

# --- Функции генерации ошибочных данных ---

def generate_valid_email(domain: str = "testmail.com") -> str:
    """Генерирует корректный email"""
    usernames = ["testuser", "qauser", "autotest", "selenium", "tester"]
    username = random.choice(usernames)
    timestamp = str(int(time.time() * 1000))[-6:]
    return f"{username}_{timestamp}@{domain}"


def generate_invalid_password() -> str:
    """Генерирует пароль короче 6 символов — ошибка для теста"""
    errors = [
        '',                    # пустой пароль (0 символов)
        '123',               # 3 символа — слишком короткий
        'ab',                # 2 символа — слишком короткий
        'qwe',               # 3 символа — слишком короткий
        'pass',              # 4 символа — слишком короткий
        'test',              # 4 символа — слишком короткий
        '12',               # 2 символа — слишком короткий
        'a',                # 1 символ — слишком короткий
        '12345',           # 5 символов — на 1 символ меньше минимума
        '   ',             # пробелы вместо пароля
        'abc12',          # 5 символов — недостаточно
    ]
    return random.choice(errors)


def generate_valid_name() -> str:
    """Генерирует корректное имя"""
    names = ["Анна", "Мария", "Екатерина", "Ольга", "Наталья",
             "Ирина", "Светлана", "Юлия", "Виктория", "Елена"]
    return random.choice(names)


# --- Готовые тестовые данные с ошибкой только в пароле ---

def get_registration_data_with_password_error() -> dict:
    """Возвращает словарь с данными для регистрации, где ошибка только в пароле"""
    return {
        'name': generate_valid_name(),
        'email': generate_valid_email(),
        'password': generate_invalid_password()  # единственная ошибка — короткий пароль
    }


def get_login_data_with_password_error() -> dict:
    """Возвращает словарь с данными для входа, где ошибка только в пароле"""
    return {
        'email': generate_valid_email(),  # корректный email
        'password': generate_invalid_password()  # ошибочный (короткий) пароль
    }


# -------------Основной сценарий теста-----------------------

# инициализируем драйвер браузера
driver = webdriver.Chrome()

# Получаем данные для регистрации с ошибкой в пароле
registration_data = get_registration_data_with_password_error()

print(f"Используемый email: {registration_data['email']}")
print(f"Используемый пароль: {registration_data['password']} (намеренно некорректный)")


# Открываем страницу
driver.get('https://stellarburgers.education-services.ru')

# сделаем паузу
time.sleep(3)

# 1.Найди кнопку "Войти в аккаунт" и кликни по ней
login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_button__33qZ0")))
login_button.click()


# 2.Найди кнопку "Зарегистрироваться" и кликни по ней
register_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]")))
register_link.click()

# ----------------Ошибка при регистрации-------------

# 3.Найди поле "Имя" и заполни его
name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "fieldset.Auth_fieldset__1QzWN:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
    )
name_field.clear()
name_field.send_keys(registration_data['name']) 

# 4.Найди поле "Email" и заполни его
email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "fieldset.Auth_fieldset__1QzWN:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
    )
email_field.clear()
email_field.send_keys(registration_data['email'])

# 5.Найдим поле "Пароль" и заполни его
password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".input_type_password > input:nth-child(2)"))
    )
password_field.clear()
password_field.send_keys(registration_data['password'])


# 6.Найди кнопку "Зарегистрироваться" и кликни по ней
register_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_button__33qZ0"))
)
register_button.click()

# сделаем паузу
time.sleep(3)

# Ждём появления сообщения об ошибке
error_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__error")))

# Проверяем текст ошибки
assert 'Некорректный пароль' in error_message.text, \
        f"❌ Ошибка: текст 'Некорректный пароль' не найден. Найден текст: '{error_message.text}'"
print("✅ Получаем ошибку 'Некорректный пароль'")

# сделаем паузу
time.sleep(3)

driver.quit()