from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from test_data import load_credentials_csv

# Инициализируем драйвер браузера
driver = webdriver.Chrome()

# --------Этап 1: Загрузка сохранённых данных password and email-------
saved_users = load_credentials_csv()
if not saved_users:
    raise Exception("❌ Нет сохранённых учётных данных. Сначала запустите тест регистрации!")

# Дополнительная проверка: убеждаемся, что есть хотя бы один пользователь
if len(saved_users) == 0:
    raise Exception("❌ Список пользователей пуст — в файле нет данных для входа!")

# Берём последнего зарегистрированного пользователя (последняя строка в CSV)
login_data = saved_users[-1]
print(f"Используем данные для входа: {login_data['name']} ({login_data['email']})")

# Открываем страницу 
driver.get('https://stellarburgers.education-services.ru')

# сделаем паузу
time.sleep(3)
# -------- Успешно загрузили сохранённые данные password and email-------

# ----------Этап 2. Авторизация в ЛК----------------

# 1.Найди кнопку "Войти в аккаунт" и кликни по ней
login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_button__33qZ0"))
    )
login_button.click()

# 2.Находим поле "Email" и заполняем его
email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".input_type_text input"))
    )
email_field.clear()
email_field.send_keys(login_data['email'])


# 3.Найди поле "Пароль" и заполни его
password_field = driver.find_element(By.CSS_SELECTOR, ".input_type_password input")
password_field.clear()
password_field.send_keys(login_data['password'])

# 4.Найди кнопку "Войти" и кликни по ней
submit_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти')]"))
    )
submit_login_button.click()

# сделаем паузу
time.sleep(3)

# Ждём подтверждения входа - проверяем появилась ли кнопка "Оформить заказ"
order_button = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".button_button__33qZ0"))
)
assert 'Оформить заказ' in order_button.text, \
    f"❌ Ошибка: текст 'Оформить заказ' не найден в кнопке. Текст кнопки: '{order_button.text}'"
print("✅ Успешно вошли в аккаунт!")

# сделаем паузу
time.sleep(3)
# -------------------------Успешная Авторизация в ЛК----------------

# -----------------Этап 3. Задание Проверь переход из ЛК по клику на «Конструктор»-----------

# 5.Кликаем кнопку «Перейти в ЛК»
profile_link = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AppHeader_header__link__3D_hX:nth-child(3) > p:nth-child(2)"))
)
profile_link.click() 
print("✅ Выполнен переход по клику на «Личный кабинет»")

# сделаем паузу
time.sleep(3)

# Проверяем действительно ли мы в ЛК - проверим появилось надпись "В этом разделе вы можете изменить свои персональные данные"
personal_button = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".Account_text__fZAIn"))
)

assert 'В этом разделе вы можете изменить свои персональные данные' in personal_button.text, \
    f"❌ Ошибка: текст 'В этом разделе вы можете изменить свои персональные данные' не найден. Найденный текст: '{personal_button.text}'"
print("✅ Подтверждено: мы находимся в личном кабинете")

# сделаем паузу
time.sleep(3)

# 6.Найди кнопку "Логотип Бургера" и кликни по ней
logo_link = driver.find_element(By.CSS_SELECTOR, ".AppHeader_header__logo__2D0X2 > a")
logo_link.click()

# Ждём возврата к главной странице - проверяем появилась ли кнопка "Оформить заказ"
order_button = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".button_button__33qZ0"))
)
assert 'Оформить заказ' in order_button.text, \
    f"❌ Ошибка: текст 'Оформить заказ' не найден в кнопке. Текст кнопки: '{order_button.text}'"
print("✅ Нажали на кнопку 'Логотип Бургера'")

# сделаем паузу
time.sleep(3)

driver.quit()