# Локаторы для страницы регистрации
REGISTRATION_NAME_INPUT = "input[name='name']" # или input[placeholder='Имя']
REGISTRATION_EMAIL_INPUT = "input[type='email']"  # или input[type='email']
REGISTRATION_PASSWORD_INPUT = ".input_type_password > input:nth-child(2)" # или input[type='password']
REGISTRATION_SUBMIT_BUTTON = ".button_button__33qZ0" # Кнопка «Зарегистрироваться»
REGISTRATION_ERROR_MESSAGE = ".input__error" # Сообщение об ошибке

# Локаторы для страницы входа
LOGIN_EMAIL_INPUT = ".input_type_text input" # Поле Email в форме входа
LOGIN_PASSWORD_INPUT = ".input_type_password input" # Поле пароля в форме входа
LOGIN_SUBMIT_BUTTON = ".button_button__33qZ0" # Кнопка «Войти»
LOGIN_FORM_TITLE_TEXT = ".Auth_login__3hAey > h2:nth-child(1)" # Надпись «Вход» в форме входа в ЛК
LOGIN_LINK_BUTTON = ".Auth_link__1fOlj" #  переход по кнопке "Воити" через форму "Зарегистрироваться" и "Восстановление пароля"


# Локаторы главной страницы
MAIN_LOGIN_BUTTON = ".button_button__33qZ0" # Кнопка «Войти в аккаунт» на главной
PERSONAL_CABINET_BUTTON = "a.AppHeader_header__link__3D_hX:nth-child(3) > p:nth-child(2)" # Кнопка «Личный кабинет»
PLACE_ORDER_BUTTON = ".button_button__33qZ0"
CONSTRUCTOR_LOGO = ".AppHeader_header__logo__2D0X2 > a" # Логотип Stellar Burgers

# Локаторы конструктора (если нужны)
CONSTRUCTOR_BUNS_TAB = "a[href='/constructor/buns']"

# Локаторы личного кабинета
PERSONAL_CABINET_EXIT_BUTTON = ".Account_button__14Yp3" # Кнопка «Выйти» в личном кабинете
INFO_TEXT = ".Account_text__fZAIn" # Надпись «В этом разделе вы можете изменить свои персональные данные» в личном кабинете
CONSTRUCTOR_LINK_BUTTON = ".AppHeader_header__link__3D_hX:nth-child(1) > p:nth-child(2)" # Переход на страницу конструктора

# Локаторы конструктора
CONSTRUCTOR_BUNS_TAB = "div.tab_tab__1SPyG:nth-child(1)"  # Вкладка «Булки»
ACTIVE_BUN_TEXT = "ul.BurgerIngredients_ingredients__list__2A-mT:nth-child(2) > a:nth-child(1) > p:nth-child(4)" # Вкладка «Булки» - надпись "Флюоресцентная булка"
CONSTRUCTOR_SAUCES_TAB = "div.tab_tab__1SPyG:nth-child(2)"  # Вкладка «Соусы»
ACTIVE_SAUCE_TEXT = "ul.BurgerIngredients_ingredients__list__2A-mT:nth-child(4) > a:nth-child(1) > p:nth-child(4)" # Вкладка «СОУСЫ» - надпись "Spicy-X"
CONSTRUCTOR_FILLINGS_TAB = "div.tab_tab__1SPyG:nth-child(3)"  # Вкладка «Начинки»
ACTIVE_FILLINGS_TEXT = "ul.BurgerIngredients_ingredients__list__2A-mT:nth-child(6) > a:nth-child(1) > p:nth-child(4)" # Вкладка «Начинки» - надпись "Мясо бессмертных молюсков"