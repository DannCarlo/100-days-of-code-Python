import time
from selenium import webdriver
from selenium.webdriver.common.by import By

SPEEDTEST_URL = "https://www.speedtest.net/"

class SpeedTest:
    def __init__(self):
        self.download_speed = None
        self.upload_speed = None

        self.driver = self.open_url()

        time.sleep(.5)

        self.run_test()

    def open_url(self):
        option = webdriver.EdgeOptions()
        option.add_experimental_option("detach", True)

        driver = webdriver.Edge(options=option)
        driver.maximize_window()
        driver.get(SPEEDTEST_URL)

        return driver

    def run_test(self):
        button = self.driver.find_element(By.CSS_SELECTOR, ".speedtest-container .start-button a")
        button.click()

        time.sleep(45)

        self.download_speed = float(self.driver.find_element(By.CSS_SELECTOR,
                                                             ".result-data-value.download-speed").text)
        self.upload_speed = float(self.driver.find_element(By.CSS_SELECTOR,
                                                           ".result-data-value.upload-speed").text)

    def exit(self):
        self.driver.quit()


