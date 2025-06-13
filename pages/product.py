from .page import Page
from selenium.webdriver.common.by import By
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class ProductPage(Page):
    def select_prod(self, product_title):
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
            for product in products:
                title_element = product.find_element(By.XPATH, ".//h4/a")
                if title_element.text.strip().lower() == product_title.strip().lower():
                    logger.info("Выбор продукта: %s", product_title)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", title_element)
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//h4/a")))
                    title_element.click()
                    return
            logger.error("Продукт не найден: %s", product_title)
            raise Exception(f"Продукт {product_title} не найден")
        except Exception as e:
            logger.error("Ошибка при выборе продукта %s: %s", product_title, str(e))
            raise Exception(f"Продукт {product_title} не найден: {str(e)}")

    def add_to_wishlist(self):
        logger.info("Добавление продукта в избранное")
        wishlist_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Добавить в закладки']"))
        )
        wishlist_button.click()

    def add_to_cart(self):
        logger.info("Добавление продукта в корзину")
        self.click(By.ID, "button-cart")

    def select_color(self, color_value):
        try:
            logger.info("Выбор цвета: %s", color_value)
            color_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "input-option226"))
            )
            color_select.click()
            color_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//select[@id='input-option226']/option[@value='{color_value}']"))
            )
            color_option.click()
            logger.info("Цвет выбран: %s", color_value)
        except Exception as e:
            logger.error("Ошибка при выборе цвета %s: %s", color_value, str(e))
            raise
