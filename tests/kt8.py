import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.extensions.action_helpers import ActionHelpers

@pytest.fixture
def driver():
    desired_caps = {
        'platformName': 'Android',
        'deviceName': 'emulator-5554',
        'app': '/Downloads/youtube.apk',
        'automationName': 'UiAutomator2',
        'noReset': True
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.__class__ = type('WebDriverWithActionHelpers', (webdriver.Remote, ActionHelpers), {})
    yield driver
    driver.quit()

def test_tap(driver):
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Home').click()
    except:
        pass
    
    search_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search')
    driver.tap([(search_button.location['x'] + 10, search_button.location['y'] + 10)])
    search_field = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/search_edit_text')
    assert search_field.is_displayed(), "Search field should be visible after tap"

def test_swipe(driver):
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Home').click()
    except:
        pass
    
    window_size = driver.get_window_size()
    start_x = window_size['width'] * 0.5
    start_y = window_size['height'] * 0.8
    end_y = window_size['height'] * 0.2
    
    driver.swipe(start_x, start_y, start_x, end_y, 500)

    try:
        new_element = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/thumbnail')
        assert new_element.is_displayed(), "New content should be visible after swipe"
    except:
        pytest.fail("Swipe action failed to load new content")

def test_multi_touch(driver):
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Home').click()
        video = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/thumbnail')
        video.click()
    except:
        pytest.fail("Failed to navigate to video player")
    
    video_player = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/player_view')
    center_x = video_player.location['x'] + video_player.size['width'] / 2
    center_y = video_player.location['y'] + video_player.size['height'] / 2
    
    action1 = TouchAction(driver).press(x=center_x, y=center_y).move_to(x=center_x + 100, y=center_y + 100)
    action2 = TouchAction(driver).press(x=center_x, y=center_y).move_to(x=center_x - 100, y=center_y - 100)
    
    driver.perform_multi_touch([action1, action2])
    
    assert video_player.is_displayed(), "Video player should remain visible after multi-touch"

def test_long_press(driver):
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Home').click()
    except:
        pass
    
    video = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/thumbnail')
    driver.long_press(video, duration=2000)
    
    context_menu = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/quick_actions_container')
    assert context_menu.is_displayed(), "Context menu should be visible after long press"

def test_drag_and_drop(driver):
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Subscriptions').click()
    except:
        pytest.fail("Failed to navigate to Subscriptions")

    try:
        channel_item = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/channel_item')
        target_y = channel_item.location['y'] - 200  
        
        driver.drag_and_drop(channel_item, channel_item.location['x'], target_y)
        new_position = driver.find_element(AppiumBy.ID, 'com.google.android.youtube:id/channel_item').location['y']
        assert abs(new_position - target_y) < 100, "Drag and drop should move item to new position"
    except:
        pytest.fail("Drag and drop action failed - element not found or not draggable")