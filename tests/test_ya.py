from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Настройка WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Открытие сайта
driver.get("https://ya.ru")

# Пауза для просмотра результата (можно убрать или настроить)
time.sleep(5)

# Закрытие браузера
driver.quit()