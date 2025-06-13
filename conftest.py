import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pages.home import HomePage
from pages.product import ProductPage
from pages.review import ReviewPage
from pages.login import LoginPage
from pages.admin import AdminPage
from pages.cart import CartPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='test_execution.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true")
    parser.addoption("--base-url", default="https://demo-opencart.ru")

@pytest.fixture(scope="module")
def base_url(request):
    logger.info("Retrieved base URL: %s", request.config.getoption("--base-url"))
    return request.config.getoption("--base-url")

def get_driver_options(browser_name, headless):
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    else:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
    logger.info("Configured driver options for browser: %s, headless: %s", browser_name, headless)
    return options

@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    options = get_driver_options(browser_name, headless)
    
    if browser_name == "chrome":
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)
    
    driver.maximize_window()
    driver.implicitly_wait(5)
    logger.info("Initialized WebDriver for browser: %s", browser_name)
    
    yield driver
    
    logger.info("Quitting WebDriver")
    driver.quit()

@pytest.fixture(scope="function")
def pages(driver, base_url):
    logger.info("Initializing page objects")
    home_page = HomePage(driver)
    home_page.navigate_to(f"{base_url}/index.php")
    
    return {
        "home_page": home_page,
        "product_page": ProductPage(driver),
        "review_page": ReviewPage(driver),
        "login_page": LoginPage(driver),
        "admin_page": AdminPage(driver),
        "cart_page": CartPage(driver)
    }

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver is not None:
            logger.error("Test %s failed: %s", item.name, rep.longrepr)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
