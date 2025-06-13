import time

class Page:
  def __init__(self, driver):
    self.driver = driver

  def click(self, by, value):
    time.sleep(1)
    element = self.driver.find_element(by, value)
    element.click()

  def send_keys(self, by, value, text):
    time.sleep(1)
    element = self.driver.find_element(by, value)
    element.send_keys(text)

  def scroll_to(self, x, y):
    self.driver.execute_script(f"window.scrollTo({x}, {y});")