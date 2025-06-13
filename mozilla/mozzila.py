import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

firefox_option = webdriver.FirefoxOptions()
firefox_option.add_argument('--start-maximized')
browser = webdriver.Firefox(options=firefox_option)

browser.get('https://demo.opencart.com/')

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//div[@id='slideshow0']")
element.click()

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//li[2]//a[1]//img[1]")
element.click()

time.sleep(0.5)

element = browser.find_element(By.XPATH, "//button[@title='Next (Right arrow key)']")
element.click()
element.click()

time.sleep(1.5)
browser.back()

time.sleep(1.5)

actions = ActionChains(browser)
PC = browser.find_element(By.XPATH,"//a[@class='dropdown-toggle'][contains(text(),'Компьютеры')]")
actions.move_to_element(PC).perform()

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//a[normalize-space()='PC (0)']")
element.click()

time.sleep(1)
browser.back()

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//a[@title='Личный кабинет']")
element.click()

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']//a[contains(text(),'Регистрация')]")
element.click()

time.sleep(1.5)

element = browser.find_element(By.XPATH, "//input[@id='register_email']")
element.send_keys("katetest1@yandex.com")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_password']")
element.send_keys("Rgtj456704")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_confirm_password']")
element.send_keys("Rgtj456704")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_firstname']")
element.send_keys("Ekaterina")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_lastname']")
element.send_keys("Polozhentseva")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_telephone']")
element.send_keys("79779368202")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//select[@id='register_country_id']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//option[@value='176']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//select[@id='register_zone_id']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//option[@value='83']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_city']")
element.send_keys("Москва")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_postcode']")
element.send_keys("14422")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@id='register_address_1']")
element.send_keys("ВДНХ")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//a[@id='simpleregister_button_confirm']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@placeholder='Поиск']")
element.click()
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//input[@placeholder='Поиск']")
element.send_keys("iphone")
time.sleep(0.5)

element = browser.find_element(By.XPATH, "//button[@class='btn btn-default btn-lg']")
element.click()
time.sleep(0.5)

input("Нажмите Enter для завершения работы")

browser.quit()
