from .page import Page
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage(Page):
    def login(self, email, password):
        try:
            user_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".fa.fa-user"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", user_icon)
            user_icon.click()

            
            login_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='https://demo-opencart.ru/index.php?route=account/login']"))
            )
            login_link.click()

           
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-email"))
            )

            logger.info("Ввод почты: %s", email)
            email_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input-email"))
            )
            email_input.clear()
            email_input.send_keys(email)
            logger.info("Ввод пароля")
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input-password"))
            )
            password_input.clear()
            password_input.send_keys(password)
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn btn-primary') and text()='Войти']"))
            )
            if login_button.get_attribute("disabled"):
                logger.error("Кнопка 'Войти' отключена")
                raise Exception("Кнопка 'Войти' отключена")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            login_button.click()

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Мой аккаунт')]"))
            )
            logger.info("Логин выполнен успешно")
        except Exception as e:
            logger.error("Ошибка при логине: %s", str(e))
            try:
                error_message = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
                )
                if error_message.is_displayed():
                    logger.error("Сообщение об ошибке логина: %s", error_message.text)
            except:
                pass
            raise
