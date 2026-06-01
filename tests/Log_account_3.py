import sys
from pathlib import Path

# Добавляем родительскую папку в путь поиска модулей
sys.path.append(str(Path(__file__).parent.parent))

# Импорты локаторов и тестовых данных
from locators import (
    MAIN_LOGIN_BUTTON,
    LOGIN_EMAIL_INPUT,
    LOGIN_PASSWORD_INPUT,
    LOGIN_SUBMIT_BUTTON,
    PERSONAL_CABINET_BUTTON
)
from test_data import existing_user

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

def test_login_via_main_button(driver):
    """
    Тест входа в личный кабинет через кнопку «Войти в аккаунт» на главной странице.
    
    Шаги:
    1. Открыть главную страницу.
    2. Нажать кнопку «Войти в аккаунт».
    3. Заполнить форму входа (email, пароль).
    4. Нажать кнопку «Войти».
    5. Проверить успешность входа (появление кнопки «Личный кабинет»).
    """

    # Шаг 1: Открытие главной страницы
    driver.get('https://stellarburgers.education-services.ru')
    logger.info("Открыта главная страница")

    # Шаг 2: Переход к форме входа
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_LOGIN_BUTTON))
    )
    login_button.click()
    logger.info("Нажата кнопка 'Войти в аккаунт'")

    # Шаг 3: Заполнение формы входа
    login_data = existing_user
    logger.info(f"Выполняем вход для пользователя: {login_data['name']}")
    logger.info(f"Email: {login_data['email']}")

    # Ввод email
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_EMAIL_INPUT))
    )
    email_field.clear()
    email_field.send_keys(login_data['email'])
    assert login_data['email'] in email_field.get_attribute("value"), "Email не введен в поле"

    # Ввод пароля
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_PASSWORD_INPUT))
    )
    password_field.clear()
    password_field.send_keys(login_data['password'])
    assert len(password_field.get_attribute("value")) > 0, "Пароль не введен"

    # Шаг 4: Нажатие кнопки входа
    submit_login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_SUBMIT_BUTTON))
    )
    submit_login_button.click()
    logger.info("Форма входа отправлена, ожидаем результат")

    # Шаг 5: Проверка успешности входа
    cabinet_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PERSONAL_CABINET_BUTTON))
    )
    assert cabinet_button.is_displayed(), "Кнопка 'Личный кабинет' не появилась — вход не выполнен"
    logger.info("✅ Успешный вход в систему: отображена кнопка 'Личный кабинет'")
