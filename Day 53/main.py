import datetime as dt
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

ZILLOW_INIT_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.53821460131836%2C%22east%22%3A-122.32844439868164%2C%22south%22%3A37.66408289599995%2C%22north%22%3A37.886333979769425%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22priorityscore%22%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A578882%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%7D"

listings_data = {
    "datetime" : [],
    "address" : [],
    "price" : [],
    "link" : []
}

option = webdriver.EdgeOptions()
option.add_experimental_option("detach", True)

driver = webdriver.Edge(options=option)
driver.maximize_window()
driver.get(ZILLOW_INIT_URL)

webscrape_start_index = 1

while webscrape_start_index < 8:
    time.sleep(7)

    scroll_container = driver.find_element(By.CSS_SELECTOR, "#grid-search-results")
    scroll_container.click()

    for _ in range(200):
        ActionChains(driver).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()

    time.sleep(1)

    next_link_button = driver.find_element(By.CSS_SELECTOR, ".search-pagination nav ul li:last-of-type a")

    listing_containers = driver.find_elements(By.XPATH, "//*[@id=\"grid-search-results\"]/ul/li")
    for listing in listing_containers:
        datetime_now = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            address = listing.find_element(By.CSS_SELECTOR, "a address").text
            price = listing.find_element(By.CSS_SELECTOR, "span").text
            link = listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            pass
        else:
            if address not in listings_data["address"]:
                listings_data["datetime"].append(datetime_now)
                listings_data["address"].append(address)
                listings_data["price"].append(price)
                listings_data["link"].append(link)

    next_link_button.click()
    webscrape_start_index += 1
    print(listings_data)

listings_dataframe = pd.DataFrame.from_dict(listings_data)

listings_dataframe.to_csv("listings.csv", index=False)


