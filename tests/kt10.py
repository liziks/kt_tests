import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

# 1. Тест успешного входа
def test_valid_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "You logged into a secure area!" in driver.page_source

# 2. Тест входа с неверным паролем
def test_invalid_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Your password is invalid!" in driver.page_source

# 3. Тест работы с чекбоксами
def test_checkboxes(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for checkbox in checkboxes:
        checkbox.click()
    assert all(checkbox.is_selected() for checkbox in checkboxes)

# 4. Тест выпадающего списка
def test_dropdown(driver):
    driver.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 1")
    assert dropdown.first_selected_option.text == "Option 1"
    dropdown.select_by_value("2")
    assert dropdown.first_selected_option.text == "Option 2"

# 5. Тест загрузки файла
def test_file_upload(driver):

    with open("test_file.txt", "w") as f:
        f.write("Test file content")
    
    driver.get("https://the-internet.herokuapp.com/upload")
    driver.find_element(By.ID, "file-upload").send_keys(os.path.abspath("test_file.txt"))
    driver.find_element(By.ID, "file-submit").click()
    assert "File Uploaded!" in driver.page_source

    os.remove("test_file.txt")

# 6. Тест динамической загрузки
def test_dynamic_loading(driver):
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "finish"))
    )
    assert "Hello World!" in driver.page_source

# 7. Тест JavaScript-алертов
def test_js_alerts(driver):
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    driver.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    alert = driver.switch_to.alert
    assert alert.text == "I am a JS Alert"
    alert.accept()
    assert "You successfully clicked an alert" in driver.page_source

# 8. Тест наведения курсора
def test_hovers(driver):
    driver.get("https://the-internet.herokuapp.com/hovers")
    avatar = driver.find_element(By.CSS_SELECTOR, ".figure")
    ActionChains(driver).move_to_element(avatar).perform()
    assert "user1" in driver.find_element(By.CSS_SELECTOR, ".figcaption").text

# 9. Тест множественных вкладок
def test_multiple_windows(driver):
    driver.get("https://the-internet.herokuapp.com/windows")
    driver.find_element(By.LINK_TEXT, "Click Here").click()
    driver.switch_to.window(driver.window_handles[1])
    assert "New Window" in driver.title
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# 10. Тест перетаскивания (Drag and Drop)
def test_drag_and_drop(driver):
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    source = driver.find_element(By.ID, "column-a")
    target = driver.find_element(By.ID, "column-b")
    ActionChains(driver).drag_and_drop(source, target).perform()
    assert "B" in source.text