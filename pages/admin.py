from .page import Page
from selenium.webdriver.common.by import By
import time

class AdminPage(Page):
    menu_selector = {
        "Catalog": "1",
        "Extensions": "2",
        "Design": "3",
        "Sales": "4",
        "Customers": "5",
        "Marketing": "6",
        "System": "7",
        "Reports": "8"}
    submenu_selector = {
        "Categories": "category",
        "Products": "product",
        "Subscription Plans": "subscription_plan",
        "Filters": "filter",
        "Attributes": "attribute",
        "Attribute Groups": "attribute_group",
        "Options": "option",
        "Manufacturers": "manufacturer",
        "Downloads": "download",
        "Reviews": "review",
        "Information": "information"
    }

    def scroll_down(self, pixels):
        self.scroll_to(0, pixels)

    def scroll_up(self, pixels):
        self.scroll_to(pixels, 0) 

    def navigate_to_admin(self, url):
        self.driver.get("https://demo-opencart.ru/admin/index.php")

    def login(self, email, password):
        time.sleep(1)        
        self.send_keys(By.ID, "input-username", email)
        self.send_keys(By.ID, "input-password", password)
        self.click(By.CSS_SELECTOR, ".btn.btn-primary")

    def click_navigate(self, menu_item):
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//a[@href='#collapse-{self.menu_selector[menu_item]}']").click()

    def click_navigate_new(self, menu_item):
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//a[@href='#collapse{self.menu_selector[menu_item]}']").click()

    def click_submenu_item(self, submenu_item):
        submenu_url_part = self.submenu_selector[submenu_item]
        submenu_item_element = self.driver.find_element(By.XPATH, f"//a[contains(@href, '{submenu_url_part}')]")
        submenu_item_element.click()

    def add_new(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()

    def add_new_category(self, name):
        self.driver.find_element(By.ID, "input-name-1").send_keys(name)
        time.sleep(1)
        self.driver.find_element(By.ID, "input-meta-title-1").send_keys(name)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[@href='#tab-seo']").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "input-keyword-0-1").send_keys(name)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()

    def add_new_category_new(self, name):
        self.driver.find_element(By.ID, "input-name1").send_keys(name)
        time.sleep(1)
        self.driver.find_element(By.ID, "input-meta-title1").send_keys(name)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[@href='#tab-seo']").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
    
    def add_new_product(self, name, category, price):
        self.driver.find_element(By.ID, "input-name-1").send_keys(name)
        time.sleep(1) 
        self.driver.find_element(By.ID, "input-meta-title-1").send_keys(name)
        time.sleep(1) 
        self.driver.find_element(By.XPATH, "//a[@href='#tab-data']").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "input-model").send_keys(name)
        time.sleep(1) 
        self.driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)
        self.driver.find_element(By.ID, "input-price").send_keys(price)
        time.sleep(1) 
        self.driver.execute_script("window.scrollTo(300, 0);")
        time.sleep(1)        
        self.driver.find_element(By.XPATH, "//a[@href='#tab-links']").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "input-category").send_keys(category)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[@href='#tab-seo']").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "input-keyword-0-1").send_keys(name)
        time.sleep(1)      
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()   
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-light").click()   

    def page_select(self, num):
        self.driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//li[contains(@class, 'page-item')]/a[text()='{num}']").click()
        time.sleep(1)
    
    def page_select_new(self, num):
        self.driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//a[text()='{num}']").click()
        time.sleep(1)

    def select_product(self, name):
        time.sleep(1)

        rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            product_name_elem = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
            if name.strip().lower() in product_name_elem.text.strip().lower():
                checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                checkbox.click()

    def delete_product(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-danger").click()
        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)

    def back(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-light").click() 

    def back_new(self):
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-default").click()
