from .page import Page
from selenium.webdriver.common.by import By
import time

class CartPage(Page):
    def navigate_to_cart(self):
        self.click(By.XPATH, "//a[@href='https://demo-opencart.ru/index.php?route=checkout/cart']")
        time.sleep(1)

    def verify_product_in_cart(self, product_title):
        product = self.driver.find_element(By.XPATH, f"//td[contains(text(), '{product_title}')]")
        assert product is not None, f"Product {product_title} not found in cart"
        time.sleep(1)

    def remove_from_cart(self, product_title):
        self.click(By.XPATH, f"//a[contains(text(), '{product_title}')]//following-sibling::button")
        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)