import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for CI
    options.add_argument('--window-size=375,812')  # Mobile viewport size
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://m.youtube.com')
    yield driver
    driver.quit()

def test_search_functionality(driver):
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Search"]'))
    )
    search_button.click()
    
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]'))
    )
    search_input.send_keys('test video')
    search_input.send_keys(Keys.RETURN)
    
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytm-video-with-context-renderer'))
    )
    assert len(results) > 0, "Search should return at least one result"

def test_video_playback(driver):
    first_video = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytm-video-with-context-renderer'))
    )
    first_video.click()
    
    player = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.html5-video-player'))
    )
    assert player.is_displayed(), "Video player should be visible after clicking video"

def test_scroll_behavior(driver):
    initial_videos = driver.find_elements(By.CSS_SELECTOR, 'ytm-video-with-context-renderer')
    initial_count = len(initial_videos)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ytm-video-with-context-renderer')) > initial_count
    )
    
    new_videos = driver.find_elements(By.CSS_SELECTOR, 'ytm-video-with-context-renderer')
    assert len(new_videos) > initial_count, "More videos should load after scrolling"

def test_hamburger_menu(driver):
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Guide"]'))
    )
    menu_button.click()
    
    menu_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytm-pivot-bar-item-renderer'))
    )
    assert len(menu_items) > 3, "Menu should contain multiple items"

def test_responsive_design(driver):
    initial_videos_per_row = len(driver.find_elements(By.CSS_SELECTOR, 'ytm-rich-item-renderer'))
    
    driver.set_window_size(768, 1024)

    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ytm-rich-item-renderer')) != initial_videos_per_row
    )
    
    new_videos_per_row = len(driver.find_elements(By.CSS_SELECTOR, 'ytm-rich-item-renderer'))
    assert new_videos_per_row != initial_videos_per_row, "Layout should change based on viewport size"