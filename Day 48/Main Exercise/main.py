from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime as dt

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie_element = driver.find_element(By.CSS_SELECTOR, "#cookie")

cookies_element = driver.find_element(By.CSS_SELECTOR, "#cps")

minutes_after_5secs = dt.datetime.now() + dt.timedelta(seconds=5)

minutes_after_5mins = dt.datetime.now() + dt.timedelta(minutes=5)

while dt.datetime.now() < minutes_after_5mins:
    cookie_element.click()
    if dt.datetime.now() >= minutes_after_5secs:
        most_expensive_helper_list = driver.find_elements(By.CSS_SELECTOR, "#store > :not(.grayed)")
        most_expensive_helper = most_expensive_helper_list[len(most_expensive_helper_list) - 1]
        most_expensive_helper.click()

        print(cookies_element.text)

        minutes_after_5secs += dt.timedelta(seconds=5)

print(cookies_element.text)