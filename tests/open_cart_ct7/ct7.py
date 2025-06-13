import time
import logging
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

@pytest.mark.title("Тест 1: Добавить iPhone в корзину")
def test_1(pages):
    logger.info("Тест 1: Добавить iPhone в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: iPhone")
    product_page.select_prod("iPhone")
    time.sleep(2)

    logger.info("Добавление iPhone в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 2: Добавить Canon EOS 5D в корзину с выбором цвета")
def test_2(pages):
    logger.info("Тест 2: Добавить Canon EOS 5D в корзину с выбором цвета")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Камеры")
    home_page.click_catalog_new("cameras")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: Canon EOS 5D")
    product_page.select_prod("Canon EOS 5D")
    time.sleep(2)

    logger.info("Выбор цвета")
    product_page.select_color("10")  # Red
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 3: Добавить Samsung Galaxy Tab 10.1 в корзину")
def test_3(pages):
    logger.info("Тест 3: Добавить Samsung Galaxy Tab 10.1 в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Планшеты")
    home_page.click_catalog_new("tablet")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: Samsung Galaxy Tab 10.1")
    product_page.select_prod("Samsung Galaxy Tab 10.1")
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 4: Добавить HTC Touch HD в корзину")
def test_4(pages):
    logger.info("Тест 4: Добавить HTC Touch HD в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Смартфоны")
    home_page.click_catalog_new("smartphone")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: HTC Touch HD")
    product_page.select_prod("HTC Touch HD")
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 5: Написать отзыв для iPhone")
def test_5(pages):
    logger.info("Тест 5: Написать отзыв для iPhone")
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    review_page = pages["review_page"]

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: iPhone")
    product_page.select_prod("iPhone")
    time.sleep(2)

    logger.info("Переход на вкладку Отзывы")
    review_page.click_review()
    time.sleep(2)

    logger.info("Написание отзыва")
    review_page.write_review("Great phone!", "Test User", "5")
    time.sleep(2)

    logger.info("Проверка формы отзыва")
    review_form = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.ID, "form-review"))
    )
    assert review_form.is_displayed(), "Форма отзыва не отображается"

@pytest.mark.title("Тест 6: Добавить iPhone в корзину")
def test_6(pages):
    logger.info("Тест 6: Добавить iPhone в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: iPhone")
    product_page.select_prod("iPhone")
    time.sleep(2)

    logger.info("Добавление iPhone в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 7: Добавить Canon EOS 5D в корзину")
def test_7(pages):
    logger.info("Тест 7: Добавить Canon EOS 5D в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Камеры")
    home_page.click_catalog_new("cameras")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: Canon EOS 5D")
    product_page.select_prod("Canon EOS 5D")
    time.sleep(2)

    logger.info("Выбор цвета")
    product_page.select_color("10")  # Red
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 8: Добавить Samsung Galaxy Tab 10.1 в корзину")
def test_8(pages):
    logger.info("Тест 8: Добавить Samsung Galaxy Tab 10.1 в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Планшеты")
    home_page.click_catalog_new("tablet")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: Samsung Galaxy Tab 10.1")
    product_page.select_prod("Samsung Galaxy Tab 10.1")
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 9: Добавить HTC Touch HD в корзину")
def test_9(pages):
    logger.info("Тест 9: Добавить HTC Touch HD в корзину")
    home_page = pages["home_page"]
    product_page = pages["product_page"]

    logger.info("Переход в категорию Смартфоны")
    home_page.click_catalog_new("smartphone")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: HTC Touch HD")
    product_page.select_prod("HTC Touch HD")
    time.sleep(2)

    logger.info("Добавление в корзину")
    product_page.add_to_cart()
    time.sleep(2)

    logger.info("Проверка сообщения об успехе")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в корзину" in success_alert.text.lower(), "Не удалось добавить в корзину"

@pytest.mark.title("Тест 10: Написать отзыв для iPhone")
def test_10(pages):
    logger.info("Тест 10: Написать отзыв для iPhone")
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    review_page = pages["review_page"]

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: iPhone")
    product_page.select_prod("iPhone")
    time.sleep(2)

    logger.info("Переход на вкладку Отзывы")
    review_page.click_review()
    time.sleep(2)

    logger.info("Написание отзыва")
    review_page.write_review("Great phone!", "Test User", "5")
    time.sleep(2)

    logger.info("Проверка формы отзыва")
    review_form = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.ID, "form-review"))
    )
    assert review_form.is_displayed(), "Форма отзыва не отображается"

@pytest.mark.title("Тест 11: Логин с почтой K4t3a@gmail.com")
def test_11(pages):
    logger.info("Тест 11: Логин с почтой K4t3a@gmail.com")
    home_page = pages["home_page"]
    login_page = pages["login_page"]

    logger.info("Переход на страницу логина")
    home_page.navigate_to("https://demo-opencart.ru/index.php?route=account/login")
    time.sleep(2)

    logger.info("Ввод почты и пароля")
    login_page.login("K4t3a@gmail.com", "password123")
    time.sleep(2)

    logger.info("Проверка успешного логина")
    account_link = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Мой аккаунт')]"))
    )
    assert account_link.is_displayed(), "Логин не выполнен"

@pytest.mark.title("Тест 12: Добавить iPhone в вишлист после логина")
def test_12(pages):
    logger.info("Тест 12: Добавить iPhone в вишлист после логина")
    home_page = pages["home_page"]
    login_page = pages["login_page"]
    product_page = pages["product_page"]

    logger.info("Переход на страницу логина")
    home_page.navigate_to("https://demo-opencart.ru/index.php?route=account/login")
    time.sleep(2)

    logger.info("Ввод почты и пароля")
    login_page.login("K4t3a@gmail.com", "password123")
    time.sleep(2)

    logger.info("Прокрутка вниз на 300 пикселей")
    home_page.scroll_down(300)
    time.sleep(2)

    logger.info("Выбор продукта: iPhone")
    product_page.select_prod("iPhone")
    time.sleep(2)

    logger.info("Добавление в вишлист")
    product_page.add_to_wishlist()
    time.sleep(2)

    logger.info("Проверка уведомления")
    success_alert = WebDriverWait(home_page.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "добавлен в закладки" in success_alert.text.lower(), "Не удалось добавить в вишлист"
