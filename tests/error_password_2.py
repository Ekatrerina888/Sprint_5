import sys
from pathlib import Path

# Добавляем родительскую папку в путь поиска модулей
sys.path.append(str(Path(__file__).parent.parent))

# Импорты локаторов и тестовых данных
from locators import (
    MAIN_LOGIN_BUTTON,
    REGISTRATION_NAME_INPUT,
    REGISTRATION_EMAIL_INPUT,
    REGISTRATION_PASSWORD_INPUT,
    REGISTRATION_SUBMIT_BUTTON,
    REGISTRATION_ERROR_MESSAGE
)
from test_data import invalid_password_user

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

def test_registration_with_invalid_password(driver):
    """
    Тест регистрации с некорректным паролем (слишком коротким).
    Ожидаемый результат: появление сообщения об ошибке.
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
    logger.info("Нажата кнопка 'Войти в аккаунт'")

    # Клик по "Зарегистрироваться"
    register_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Зарегистрироваться"))
    )
    register_link.click()
    logger.info("Нажата ссылка 'Зарегистрироваться'")

    # Шаг 3: Заполнение формы регистрации
    registration_data = invalid_password_user
    logger.info(f"Начинаем регистрацию с некорректным паролем: {registration_data['name']}")
    logger.info(f"Email: {registration_data['email']}")
    logger.info(f"Пароль (ожидаемая ошибка): {registration_data['password']}")

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

    # Ввод пароля (некорректного)
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
    logger.info("Форма отправлена, ожидаем сообщение об ошибке")

    # Шаг 5: Проверка появления ошибки
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, REGISTRATION_ERROR_MESSAGE))
    )
    assert 'Некорректный пароль' in error_message.text, \
        f"❌ Ошибка: текст 'Некорректный пароль' не найден. Найден текст: '{error_message.text}'"
    logger.info("✅ Успешно получено сообщение об ошибке: 'Некорректный пароль'")
