from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from test_data import get_registration_data, save_credentials_csv

# Инициализируем драйвер браузера
driver = webdriver.Chrome()

# Открываем страницу — исправлен URL
driver.get('https://stellarburgers.education-services.ru')

# 1. Найди кнопку "Войти в аккаунт" и кликни по ней
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_button__33qZ0"))
)
login_button.click()

# 2. Находим кнопку "Зарегистрироваться" и кликаем
register_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]"))
)
register_link.click()


# ----------------"Этап 1. Регистрация нового пользователя (успешная регистрация)-------
# --------Получаем данные для входа из test_data-------
registration_data = get_registration_data()

print(f"Регистрируем пользователя: {registration_data['name']}")
print(f"Email: {registration_data['email']}")
print(f"Пароль: {registration_data['password']}")

# ---------------Заполняем форму регистрации--------------------
# Поле имени
name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "fieldset.Auth_fieldset__1QzWN:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
    )
name_field.clear()
name_field.send_keys(registration_data['name'])  


# Поле email
email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "fieldset.Auth_fieldset__1QzWN:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)"))
    )
email_field.clear()
email_field.send_keys(registration_data['email'])

# Поле пароля
password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".input_type_password > input:nth-child(2)"))
    )
password_field.clear()
password_field.send_keys(registration_data['password'])

# Кликаем кнопку "Зарегистрироваться"
register_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_button__33qZ0"))
)
register_button.click()

# сделаем паузу
time.sleep(3)

# Ждём подтверждения регистрации - проверяем появилась ли форма "Вход"
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".Auth_login__3hAey > h2:nth-child(1)"))
)
print("✅ Успешно 'Зарегистрировались в ЛК'!")

# сделаем паузу
time.sleep(3)

# --------СОХРАНЕНИЕ ЗАРЕГИСТРИРОВАННЫХ ДАННЫХ ДЛЯ ДАЛЬНЕЙШЕЙ АВТОРИЗАЦИИ-------
save_credentials_csv(registration_data)
print("💾 Данные зарегистрированного пользователя сохранены в test_credentials.csv")

driver.quit()