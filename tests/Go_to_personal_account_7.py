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
    PERSONAL_CABINET_BUTTON,
    LOGIN_FORM_TITLE_TEXT,
    INFO_TEXT,
    PLACE_ORDER_BUTTON
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

def test_personal_cabinet_access(driver):
    """
    Тест перехода в личный кабинет после авторизации.

    Шаги:
    1. Открыть главную страницу.
    2. Перейти к форме входа через кнопку «Войти в аккаунт».
    3. Заполнить форму входа (email, пароль).
    4. Нажать кнопку «Войти».
    5. Проверить успешность входа (появление кнопки «Оформить заказ»).
    6. Перейти в личный кабинет через кнопку «Личный кабинет».
    7. Проверить, что отобразился контент личного кабинета - кнопка "Выход".
    """

    # Шаг 1: Открытие главной страницы
    driver.get('https://stellarburgers.education-services.ru')
    logger.info("Открыта главная страница")

    # Шаг 2: Переход к форме входа через кнопку «Войти в аккаунт»
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_LOGIN_BUTTON))
    )
    login_button.click()
    logger.info("Нажата кнопка 'Войти в аккаунт' на главной странице")

    # Дополнительная проверка: убеждаемся, что открылась форма входа
    login_form_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_FORM_TITLE_TEXT))
    )
    assert "Вход" in login_form_title.text, "Форма входа не открылась после клика на 'Войти в аккаунт'"
    logger.info("Отображена форма входа")

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
    assert login_data['email'] in email_field.get_attribute("value"), "Email не введён в поле"

    # Ввод пароля
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_PASSWORD_INPUT))
    )
    password_field.clear()
    password_field.send_keys(login_data['password'])
    assert len(password_field.get_attribute("value")) > 0, "Пароль не введён"

    # Шаг 4: Нажатие кнопки входа
    submit_login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_SUBMIT_BUTTON))
    )
    submit_login_button.click()
    logger.info("Форма входа отправлена, ожидаем результат")

    # Шаг 5: Проверка успешности входа
    exit_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
    )
    assert exit_button.is_displayed(), "Кнопка 'Оформить заказ' не появилась — вход не выполнен"
    logger.info("✅ Успешный вход в систему: отображена кнопка 'Оформить заказ' в личном кабинете")

    # Шаг 6: Переход в личный кабинет
    profile_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PERSONAL_CABINET_BUTTON))
    )
    profile_link.click()
    logger.info("Выполнен переход по клику на «Личный кабинет»")

    # Шаг 7: Проверка отображения контента личного кабинета
    personal_info_text = WebDriverWait(driver, 25).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, INFO_TEXT))
    )
    expected_text = "В этом разделе вы можете изменить свои персональные данные"
    assert expected_text in personal_info_text.text, \
        f"Текст '{expected_text}' не найден в ЛК. Найденный текст: '{personal_info_text.text}'"
    logger.info("✅ Подтверждено: мы находимся в личном кабинете")