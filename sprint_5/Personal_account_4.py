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

# --------Этап 2. Задание: вход через кнопку «Личный кабинет» на главной----------
# -----------Вход в ЛК через кнопку «Личный кабинет»------------------------------

# 1.Найди кнопку "Личный кабинет" и кликни по ней
profile_link = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AppHeader_header__link__3D_hX:nth-child(3) > p:nth-child(2)"))
)
profile_link.click() 
print("✅ Выполнен переход по клику на «Личный кабинет»")

# 2.Найди поле "Email" и заполни его
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

# 5. Ждём загрузки после входа
WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.AppHeader_header__link__3D_hX"))
    )
print("✅ Успешно вошли в систему!")

# -----------Вошли в ЛК через кнопку «Личный кабинет»-----------

driver.quit()