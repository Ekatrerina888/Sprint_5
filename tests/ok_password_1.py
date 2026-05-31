import sys
from pathlib import Path

# Добавляем родительскую папку в путь поиска модулей
sys.path.append(str(Path(__file__).parent.parent))

# Корректные импорты
from locators import (
    MAIN_LOGIN_BUTTON,
    REGISTRATION_NAME_INPUT,
    REGISTRATION_EMAIL_INPUT,
    REGISTRATION_PASSWORD_INPUT,
    LOGIN_FORM_TITLE_TEXT,
    REGISTRATION_SUBMIT_BUTTON
)

from test_data import password_user, generate_email

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия драйвера."""
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def get_registration_data():
    """Возвращает тестовые данные для регистрации."""
    return password_user

def test_registration_success(driver):
    """
    Тест успешной регистрации нового пользователя.

    Шаги:
    1. Открыть главную страницу.
    2. Перейти на страницу регистрации через кнопку «Войти» -> «Зарегистрироваться».
    3. Заполнить форму регистрации (имя, email, пароль).
    4. Нажать кнопку «Зарегистрироваться».
    5. Проверить успешность регистрации (появление формы входа).
    """

    # Шаг 1: Открытие главной страницы
    driver.get('https://stellarburgers.education-services.ru')
    logger.info("Открыта главная страница")

    # Шаг 2: Переход к регистрации
    # Клик по "Войти в аккаунт"
    login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_LOGIN_BUTTON))
    )
    login_button.click()

    # Клик по "Зарегистрироваться"
    register_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))
    )
    register_link.click()

    
    # Шаг 3: Заполнение формы регистрации
    registration_data = get_registration_data()
    logger.info(f"Начинаем регистрацию пользователя: {registration_data['name']}")
    logger.info(f"Email: {registration_data['email']}")
    logger.info(f"Пароль: {registration_data['password']}")

    # Ввод имени
    name_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, REGISTRATION_NAME_INPUT))
    )
    name_field.clear()
    name_field.send_keys(registration_data['name'])
    assert registration_data['name'] in name_field.get_attribute("value"), "Имя не введено в поле"

    # Ввод email
    email_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, REGISTRATION_EMAIL_INPUT))
    )
    email_field.clear()
    email_field.send_keys(registration_data['email'])
    assert registration_data['email'] in email_field.get_attribute("value"), "Email не введен в поле"

    # Ввод пароля
    password_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, REGISTRATION_PASSWORD_INPUT))
    )
    password_field.clear()
    password_field.send_keys(registration_data['password'])
    assert len(password_field.get_attribute("value")) > 0, "Пароль не введен"

    # Шаг 4: Нажатие кнопки регистрации
    register_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, REGISTRATION_SUBMIT_BUTTON))
    )
    register_button.click()
    logger.info("Форма отправлена, ожидаем результат")

    # Шаг 5: Проверка успешности регистрации
    success_login_form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_FORM_TITLE_TEXT))
    )
    assert success_login_form.is_displayed(), "Форма входа не появилась — регистрация не прошла"
    logger.info("✅ Успешная регистрация: отображена форма входа")





