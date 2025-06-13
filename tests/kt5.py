import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_1_create_category(pages):
    admin_page = pages["admin_page"]
    admin_page.login("demo", "demo")
    admin_page.click_navigate("Catalog")
    admin_page.click_submenu_item("Categories")
    admin_page.add_new()
    admin_page.add_new_category("Devices")
    admin_page.back()

    # Проверка создания категории
    admin_page.click_navigate("Catalog")
    admin_page.click_submenu_item("Categories")
    rows = WebDriverWait(admin_page.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )
    assert any("Devices" in row.text for row in rows), "'Devices' not found"

def test_2_add_products(pages):
    admin_page = pages["admin_page"]
    admin_page.login("demo", "demo")
    admin_page.click_navigate("Catalog")
    admin_page.click_submenu_item("Products")

    products = [
        ("mouse1", "This is a high-quality mouse1", "300"),
        ("mouse2", "This is a high-quality mouse2", "450"),
        ("keyboard1", "This is a high-quality keyboard1", "650"),
        ("keyboard2", "This is a high-quality keyboard2", "1200")
    ]
    for name, description, price in products:
        admin_page.add_new()
        admin_page.add_new_product(name, "Devices", price, description)

    # Проверка добавления продуктов
    admin_page.page_select(2)
    rows = WebDriverWait(admin_page.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )
    assert all(any(name in row.text for row in rows) for name, _, _ in products), "One or more products not found"

def test_3_verify_products(pages):
    home_page = pages["home_page"]
    products = ["mouse1", "mouse2", "keyboard1", "keyboard2"]
    for name in products:
        home_page.search(name)
        items = WebDriverWait(home_page.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb h4 a"))
        )
        assert any(name in item.text for item in items), f"'{name}' not found in main page"

def test_4_delete_products(pages):
    admin_page = pages["admin_page"]
    admin_page.login("demo", "demo")
    admin_page.click_navigate("Catalog")
    admin_page.click_submenu_item("Products")
    admin_page.page_select(2)
    admin_page.select_product("mouse1")
    admin_page.select_product("keyboard1")
    admin_page.delete_product()

    # Проверка удаления
    rows = WebDriverWait(admin_page.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )
    texts = [row.text for row in rows]
    assert not any("mouse1" in t for t in texts), "'mouse1' not deleted"
    assert not any("keyboard1" in t for t in texts), "'keyboard1' not deleted"

def test_5_verify_remaining_products(pages):
    home_page = pages["home_page"]
    products_to_check = ["mouse2", "keyboard2"]
    products_to_delete = ["mouse1", "keyboard1"]
    for name in products_to_check:
        home_page.search(name)
        items = WebDriverWait(home_page.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb h4 a"))
        )
        assert any(name in item.text for item in items), f"'{name}' not found in main page"
    for name in products_to_delete:
        home_page.search(name)
        items = WebDriverWait(home_page.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb h4 a"))
        )
        assert not any(name in item.text for item in items), f"'{name}' should be deleted"