import os
import requests
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = os.environ.get("URL")

HEADERS = {
    "User-agent" : ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"),
    "Accept" : "text/html",
    "sec-ch-ua" : "Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24"
}

def add_rows_to_csv_list():
    global csv_list, driver

    containers = driver.find_elements(By.XPATH, "//*[@id=\"__next\"]/div/div[1]/article/div[2]/table/tbody/tr")

    for container in containers:
        row_data = [element.text for element in container.find_elements(By.CSS_SELECTOR, ".data-table__value")]
        csv_list.append(row_data)

option = webdriver.EdgeOptions()
option.add_experimental_option("detach", True)

driver = webdriver.Edge(options=option)
driver.maximize_window()
driver.get(URL)

time.sleep(2)

next_href_elem = driver.find_element(By.CSS_SELECTOR, ".pagination .pagination__next-btn")
next_href = next_href_elem.get_attribute("href")

csv_list = []

column_labels_list = [element.text for element in driver.find_elements(By.XPATH, "//*[@id=\"__next\"]/div/div[1]/"
                                                    "article/div[2]/table/thead/tr/th")]
csv_list.append(column_labels_list)

add_rows_to_csv_list()

while next_href:
    next_href_elem.click()

    time.sleep(3)

    add_rows_to_csv_list()

    next_href_elem = driver.find_element(By.CSS_SELECTOR, ".pagination .pagination__next-btn")
    next_href = next_href_elem.get_attribute("href")

with open("data.csv", mode="w", newline="") as file:
        csv_data = csv.writer(file, delimiter=",")
        csv_data.writerows(csv_list)
