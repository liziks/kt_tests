import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CalculatorTests(unittest.TestCase):

    def setUp(self):
        desired_caps = {
            "platformName": "Android",
            "deviceName": "Android Emulator",
            "appPackage": "com.android.calculator2", 
            "appActivity": "com.android.calculator2.Calculator",  
            "automationName": "UiAutomator2"
        }
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    def tearDown(self):
        self.driver.quit()

    def click(self, value):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, value))
        )
        element.click()

    def get_result(self):
        result = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.android.calculator2:id/result"))
        )
        return result.text

    def test_addition(self):
        self.click("1")
        self.click("plus")
        self.click("1")
        self.click("equals")
        self.assertEqual(self.get_result(), "2", "Addition failed")

    def test_subtraction(self):
        self.click("1")
        self.click("minus")
        self.click("1")
        self.click("equals")
        self.assertEqual(self.get_result(), "0", "Subtraction failed")

    def test_multiplication(self):
        self.click("1")
        self.click("multiply")
        self.click("4")
        self.click("equals")
        self.assertEqual(self.get_result(), "4", "Multiplication failed")

    def test_division(self):
        self.click("1")
        self.click("0")
        self.click("divide")
        self.click("2")
        self.click("equals")
        self.assertEqual(self.get_result(), "5", "Division failed")

    def test_division_by_zero(self):
        self.click("1")
        self.click("divide")
        self.click("0")
        self.click("equals")
        result = self.get_result()
        self.assertTrue("Cannot" in result or "Infinity" in result, "Division by zero handling failed")

if __name__ == '__main__':
    unittest.main()