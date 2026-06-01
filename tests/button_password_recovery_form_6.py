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
    LOGIN_FORM_TITLE_TEXT,
    LOGIN_LINK_BUTTON, 
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

def test_login_via_password_recovery_form(driver):
    """
    Тест входа через кнопку в форме восстановления пароля.

    Шаги:
    1. Открыть главную страницу.
    2. Нажать кнопку «Войти в аккаунт» на главной.
    3. Перейти к форме восстановления пароля через ссылку «Восстановить пароль».
    4. Перейти обратно к форме входа через ссылку «Войти».
    5. Заполнить форму входа (email, пароль).
    6. Нажать кнопку «Войти».
    7. Проверить успешность входа (появление кнопки выхода).
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

    # Шаг 3: Переход к форме восстановления пароля
    restore_password_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Восстановить пароль"))
    )
    restore_password_link.click()
    logger.info("Перешли на страницу восстановления пароля через кнопку 'Восстановить пароль'")

    # Шаг 4: Переход к форме входа в аккаунт по кнопке "Войти"
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_LINK_BUTTON))
    )
    login_link.click()
    logger.info("Нажата кнопка 'Войти' на странице восстановления пароля")

    # Дополнительная проверка: убеждаемся, что открылась форма входа - кнопка
    login_form_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, LOGIN_FORM_TITLE_TEXT))
    )
    assert "Вход" in login_form_title.text, "Форма входа не открылась после клика на 'Войти'"
    logger.info("Отображена форма входа")

    # Шаг 5: Заполнение формы входа
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

    # Шаг 6: Нажатие кнопки входа
    submit_login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_SUBMIT_BUTTON))
    )
    submit_login_button.click()
    logger.info("Форма входа отправлена, ожидаем результат")

    # Шаг 7: Проверка успешности входа
    exit_button = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
    )
    assert exit_button.is_displayed(), "Кнопка 'Оформить заказ' не появилась — вход не выполнен"
    logger.info("✅ Успешный вход в систему: отображена кнопка 'Оформить заказ' в личном кабинете")
