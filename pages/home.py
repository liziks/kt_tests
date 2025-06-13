from .page import Page
from selenium.webdriver.common.by import By
import time
import logging

logger = logging.getLogger(__name__)

class HomePage(Page):
    catalog_new = {
        "desktop": "https://demo-opencart.ru/index.php?route=product/category&path=20",
        "laptop": "https://demo-opencart.ru/index.php?route=product/category&path=18",
        "tablet": "https://demo-opencart.ru/index.php?route=product/category&path=57",
        "software": "https://demo-opencart.ru/index.php?route=product/category&path=17",
        "smartphone": "https://demo-opencart.ru/index.php?route=product/category&path=24",
        "cameras": "https://demo-opencart.ru/index.php?route=product/category&path=33",
        "mp3": "https://demo-opencart.ru/index.php?route=product/category&path=34",
    }

    def click_catalog_new(self, product_type):
        time.sleep(1)
        logger.info("Clicking catalog link for product type: %s", product_type)
        self.click(By.XPATH, f"//a[@href='{self.catalog_new[product_type]}']")

    def navigate_to(self, url):
        logger.info("Navigating to URL: %s", url)
        self.driver.get(url)

    def click_logo(self):
        logger.info("Clicking logo")
        self.click(By.ID, "logo")

    def scroll_down(self, pixels):
        logger.info("Scrolling down by %s pixels", pixels)
        self.scroll_to(0, pixels)

    def scroll_up(self, pixels):
        logger.info("Scrolling up to %s pixels", pixels)
        self.scroll_to(pixels, 0)

    def add_to_wishlist_new(self, product_title):
        products = self.driver.find_elements(By.XPATH, "//div[@class='product-thumb']")
        for product in products:
            image = product.find_element(By.XPATH, ".//img")
            if image.get_attribute("title") == product_title:
                add_to_wishlist = product.find_element(By.XPATH, ".//button[@data-original-title='Добавить в закладки']")
                logger.info("Adding product to wishlist: %s", product_title)
                add_to_wishlist.click()
                return
        logger.error("Product not found for wishlist: %s", product_title)
        raise Exception(f"Продукт {product_title} не найден для вишлиста")

    def add_to_cart_new(self, product_title):
        products = self.driver.find_elements(By.XPATH, "//div[@class='product-thumb']")
        for product in products:
            image = product.find_element(By.XPATH, ".//img")
            if image.get_attribute("title") == product_title:
                add_to_cart_button = product.find_element(By.XPATH, ".//button[@onclick]")
                logger.info("Adding product to cart: %s", product_title)
                add_to_cart_button.click()
                return
        logger.error("Product not found for cart: %s", product_title)
