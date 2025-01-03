import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import Tk

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

links_list = []

def go_to_login_page():
    global driver

    login_a = driver.find_element(By.CSS_SELECTOR, ".sign-in-form__sign-in-cta")
    login_a.click()

    time.sleep(2)

    username_input = driver.find_element(By.NAME, "session_key")
    username_input.send_keys(EMAIL)

    password_input = driver.find_element(By.NAME, "session_password")
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, ".login__form_action_container > button")
    login_button.click()

def search_job():
    global driver

    jobs_a = driver.find_elements(By.CSS_SELECTOR, ".global-nav__primary-link")[2]
    jobs_a.click()

    time.sleep(2)

    job_input_bar = driver.find_elements(By.CSS_SELECTOR,".jobs-search-box__text-input")[0]
    job_input_bar.send_keys("Python Developer", Keys.ENTER)

    # location_input_bar = driver.find_elements(By.CSS_SELECTOR,
    #                                         ".jobs-search-box__text-input.jobs-search-box__text-input--with-clear")
    # location_input_bar.send_keys("Philippinesr")

def save_job_links():
    global driver, links_list

    jobs_container_list = driver.find_elements(By.CSS_SELECTOR, ".scaffold-layout__list ul > .ember-view")

    for job_container in jobs_container_list:
        job_container.click()

        time.sleep(.5)

        job_name = driver.find_element(By.CSS_SELECTOR, ".jobs-details__main-content "\
                                                        ".job-details-jobs-unified-top-card__job-title h1").text

        job_employer = driver.find_element(By.CSS_SELECTOR, ".jobs-details__main-content "\
                                                            ".job-details-jobs-unified-top-card__company-name > a").text

        share_button = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__top-buttons "\
                                                            ".artdeco-button")
        share_button.click()

        time.sleep(.5)

        link_button = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__top-buttons "\
                                                           ".social-share__item--copy-link")
        link_button.click()

        job_info_dict = {
            "name" : job_name,
            "employer" : job_employer,
            "link" : Tk().clipboard_get()
        }

        links_list.append(job_info_dict)

        time.sleep(.5)

def save_job_links_to_file():
    global links_list

    with open("job_links.txt", mode="w", encoding="UTF-8") as file:
        for link in links_list:
            name = link["name"]
            employer = link["employer"]
            link_text = link["link"]

            file.write(f"{name} | {employer} | {link_text}\n")

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
driver.maximize_window()
driver.get("https://linkedin.com")

time.sleep(2)

go_to_login_page()

time.sleep(2)

search_job()

time.sleep(2)

save_job_links()

save_job_links_to_file()






