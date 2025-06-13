from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_1(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    home_page.scroll_down(300)
    time.sleep(2)
    product_page.select_prod("Iphone")
    time.sleep(2)
    product_page.add_to_wishlist_new()
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert len(success_alert) > 0 and "Success: You have added" in success_alert[0].text, "Wrong result"

    time.sleep(2)
    home_page.click_logo()

def test_2(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    home_page.click_logo()
    home_page.scroll_down(1000)
    time.sleep(2)
    product_page.select_prod("Canon EOS 5D")
    product_page.select_color('15')
    home_page.scroll_down(500)
    product_page.add_to_cart()
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"
    home_page.scroll_up(0)

    home_page.click_logo()
    time.sleep(1)

def test_3(pages):
    home_page = pages["home_page"]
    home_page.click_catalog_new("tablet")
    time.sleep(1)
    home_page.scroll_down(200)
    time.sleep(2)
    home_page.add_to_cart_new("Samsung Galaxy Tab 10.1")
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"

    time.sleep(1)
    home_page.scroll_up(0)

def test_4(pages):
    home_page = pages["home_page"]
    home_page.click_catalog_new("smartphone")
    time.sleep(1)
    home_page.scroll_down(200)
    time.sleep(1)
    home_page.add_to_cart_new("HTC Touch HD")
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"

    time.sleep(2)
    home_page.scroll_up(0)

def test_5(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    review_page = pages["review_page"]
    home_page.click_catalog_new("smartphone")
    product_page.select_prod("iPhone")
    home_page.scroll_down(500)
    time.sleep(2)
    review_page.click_review()
    home_page.scroll_down(800)
    time.sleep(2)
    review_page.write_review("Review", "Nice", 4)
    time.sleep(1)

    time.sleep(2)

def test_6_add_to_wishlist(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    home_page.scroll_down(300)
    time.sleep(2)
    product_page.select_prod("iPhone")
    time.sleep(2)
    product_page.add_to_wishlist_new()
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"
    time.sleep(2)

def test_7_add_camera_to_cart(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    home_page.click_catalog_new("cameras")
    time.sleep(1)
    home_page.scroll_down(200)
    time.sleep(2)
    product_page.select_prod("Canon EOS 5D")
    product_page.add_to_cart()
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"
    time.sleep(2)

def test_8_add_tablet_to_cart(pages):
    home_page = pages["home_page"]
    home_page.click_catalog_new("tablet")
    time.sleep(1)
    home_page.scroll_down(200)
    time.sleep(2)
    home_page.add_to_cart_new("Samsung Galaxy Tab 10.1")
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"
    time.sleep(2)

def test_9_add_htc_to_cart(pages):
    home_page = pages["home_page"]
    home_page.click_catalog_new("smartphone")
    time.sleep(1)
    home_page.scroll_down(200)
    time.sleep(1)
    home_page.add_to_cart_new("HTC Touch HD")
    time.sleep(1)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: You have added" in success_alert[0].text, "Wrong result"
    time.sleep(2)

def test_10_write_review(pages):
    home_page = pages["home_page"]
    product_page = pages["product_page"]
    review_page = pages["review_page"]
    home_page.click_catalog_new("smartphone")
    time.sleep(1)
    product_page.select_prod("iPhone")
    home_page.scroll_down(500)
    time.sleep(2)
    review_page.click_review()
    home_page.scroll_down(800)
    time.sleep(2)
    review_page.write_review("TestUser", "Great phone!", 5)
    time.sleep(2)

    success_alert = home_page.driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")
    assert "Success: Your review has been submitted" in success_alert[0].text, "Review not submitted"
    time.sleep(2)
