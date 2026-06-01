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
    CONSTRUCTOR_LOGO,
    PLACE_ORDER_BUTTON,
    INFO_TEXT
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

def test_logo_navigation(driver):
    """
    Тест перехода по клику на логотип Stellar Burgers.

    Шаги:
    1. Открыть главную страницу.
    2. Авторизоваться в системе.
    3. Перейти в личный кабинет.
    4. Проверить отображение контента личного кабинета.
    5. Вернуться на главную через логотип Stellar Burgers.
    6. Проверить, что отобразилась главная страница.
    """

    # Шаг 1: Открытие главной страницы
    driver.get('https://stellarburgers.education-services.ru')
    logger.info("Открыта главная страница")

    # Шаг 2: Авторизация в системе
    # Переход к форме входа через кнопку «Войти в аккаунт»
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_LOGIN_BUTTON))
    )
    login_button.click()
    logger.info("Нажата кнопка 'Войти в аккаунт' на главной странице")

    # Заполнение формы входа
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

    # Нажатие кнопки входа
    submit_login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_SUBMIT_BUTTON))
    )
    submit_login_button.click()
    logger.info("Форма входа отправлена, ожидаем результат")

    # Проверка успешности входа (отобразилась кнопка «Оформить заказ»)
    exit_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
    )
    assert exit_button.is_displayed(), "Кнопка 'Оформить заказ' не появилась — вход не выполнен"
    logger.info("✅ Успешный вход в систему: отображена кнопка 'Оформить заказ' в личном кабинете")

    # Шаг 3: Переход в личный кабинет
    profile_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PERSONAL_CABINET_BUTTON))
    )
    profile_link.click()
    logger.info("Выполнен переход по клику на «Личный кабинет»")

    # Шаг 4: Проверка отображения контента личного кабинета
    personal_info_text = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, INFO_TEXT))
    )
    expected_text = "В этом разделе вы можете изменить свои персональные данные"
    assert expected_text in personal_info_text.text, \
        f"Текст '{expected_text}' не найден в ЛК. Найденный текст: '{personal_info_text.text}'"
    logger.info("✅ Подтверждено: мы находимся в личном кабинете")

    # Шаг 5: Возврат на главную через логотип Stellar Burgers
    logo_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONSTRUCTOR_LOGO))
    )
    logo_link.click()
    logger.info("Выполнен клик на логотип Stellar Burgers — возврат на главную")

    # Шаг 6: Проверка отображения главной страницы
    main_order_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
    )
    assert 'Оформить заказ' in main_order_button.text, \
        f"Кнопка 'Оформить заказ' не найдена на главной. Текст кнопки: '{main_order_button.text}'"
    logger.info("✅ Подтверждено: вернулись на главную страницу")
