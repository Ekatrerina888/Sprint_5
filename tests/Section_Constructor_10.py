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
    PLACE_ORDER_BUTTON,
    CONSTRUCTOR_BUNS_TAB,
    CONSTRUCTOR_SAUCES_TAB,
    CONSTRUCTOR_FILLINGS_TAB,
    ACTIVE_BUN_TEXT,
    ACTIVE_SAUCE_TEXT,
    ACTIVE_FILLINGS_TEXT
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

def test_navigation_between_constructor_sections(driver):
    """
    Тест проверки переходов между разделами конструктора: «Булки», «Соусы», «Начинки».

    Шаги:
    1. Открыть главную страницу.
    2. Авторизоваться в системе.
    3. Перейти на страницу конструктора.
    4. Проверить переход на вкладку «Булки».
    5. Проверить переход на вкладку «Соусы».
    6. Проверить переход на вкладку «Начинки».
    7. Убедиться, что все разделы отображаются корректно.
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
    order_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PLACE_ORDER_BUTTON))
    )
    assert order_button.is_displayed(), "Кнопка 'Оформить заказ' не появилась — вход не выполнен"
    logger.info("✅ Успешный вход в систему: отображена кнопка 'Оформить заказ' в личном кабинете")

    # Шаг 3: Переход на страницу конструктора
    # Используем любой элемент конструктора для перехода — например, вкладку «Соусы»
    sauce_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONSTRUCTOR_SAUCES_TAB))
    )
    sauce_tab.click()
    logger.info("Выполнен клик на вкладку 'Соусы'")

    active_sauce_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ACTIVE_SAUCE_TEXT))
    )
    assert active_sauce_tab.is_displayed(), "Вкладка 'Соусы' не стала активной после клика"
    logger.info("✅ Подтверждено: активна вкладка 'Соусы'")


    # Шаг 4: Проверка перехода на вкладку «Булки»
    bun_tab = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONSTRUCTOR_BUNS_TAB))
    )
    bun_tab.click()
    logger.info("Выполнен переход на страницу конструктора (вкладка 'Булки')")

    active_bun_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ACTIVE_BUN_TEXT))
    )
    assert active_bun_tab.is_displayed(), "Вкладка 'Булки' не стала активной после клика"
    logger.info("✅ Подтверждено: активна вкладка 'Булки'")



    # Шаг 5: Проверка перехода на вкладку «Начинки»
    filling_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, CONSTRUCTOR_FILLINGS_TAB))
    )
    filling_tab.click()
    logger.info("Выполнен клик на вкладку 'Начинки'")

    active_filling_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ACTIVE_FILLINGS_TEXT))
    )
    assert active_filling_tab.is_displayed(), "Вкладка 'Начинки' не стала активной после клика"
    logger.info("✅ Подтверждено: активна вкладка 'Начинки'")

    # Шаг 7: Финальная проверка — убедимся, что все вкладки доступны
    all_tabs = [
        (CONSTRUCTOR_BUNS_TAB, "Булки"),
        (CONSTRUCTOR_SAUCES_TAB, "Соусы"),
        (CONSTRUCTOR_FILLINGS_TAB, "Начинки")
    ]

    for tab_locator, tab_name in all_tabs:
        tab_element = driver.find_element(By.CSS_SELECTOR, tab_locator)
        assert tab_element.is_displayed(), f"Вкладка '{tab_name}' не отображается на странице конструктора"
    logger.info("✅ Все вкладки конструктора ('Булки', 'Соусы', 'Начинки') доступны и отображаются корректно")
