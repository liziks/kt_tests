from .page import Page
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class ReviewPage(Page):
    def click_review(self):
        try:
            logger.info("Клик по вкладке отзывов")
            review_tab = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#tab-review']"))
            )
            review_tab.click()
        except Exception as e:
            logger.error("Ошибка при клике по вкладке отзывов: %s", str(e))
            raise

    def write_review(self, review_text, rating_text, rating_value):
        try:
            logger.info("Написание отзыва: %s, имя: %s, рейтинг: %s", review_text, rating_text, rating_value)
            review_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input-review"))
            )
            review_input.send_keys(review_text)
            name_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input-name"))
            )
            name_input.send_keys(rating_text)
            rating_radio = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//input[@type='radio' and @value='{rating_value}']"))
            )
            rating_radio.click()
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "button-review"))
            )
            submit_button.click()
            time.sleep(2)
        except Exception as e:
            logger.error("Ошибка при написании отзыва: %s", str(e))
            raise
