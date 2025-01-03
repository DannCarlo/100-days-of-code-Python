import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
driver.get("https://www.python.org/")

data_dict = dict()

index = 0

date_element_obj = driver.find_elements(By.CSS_SELECTOR, ".event-widget .menu li")

for obj in date_element_obj:
    data_dict[index] = dict()
    year = obj.find_elements(By.CSS_SELECTOR, ".say-no-more")[0].get_attribute("innerHTML")
    date = obj.find_elements(By.CSS_SELECTOR, "time")[0].text
    name = obj.find_elements(By.CSS_SELECTOR, "a")[0].text

    data_dict[index]["time"] = year + date
    data_dict[index]["name"] = name

    index += 1

print(data_dict)
