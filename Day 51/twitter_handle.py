import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By

TWITTER_URL = "https://www.x.com"

class TwitterHandle:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

        self.driver = None

    def open_url(self):
        option = webdriver.EdgeOptions()
        option.add_experimental_option("detach", True)

        self.driver = webdriver.Edge(options=option)
        self.driver.maximize_window()
        self.driver.get(TWITTER_URL)

    def login_account(self):
        self.open_url()

        time.sleep(5)

        login_button = self.driver.find_element(By.XPATH, "//*[@id=\"react-root\"]/div/div/div[2]/main/div/div/"\
                                                 "div[1]/div[1]/div/div[3]/div[4]/a/div")
        login_button.click()

        time.sleep(3)

        username_input = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div/div/div/div"\
                                                   "/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div"\
                                                   "/div[4]/label/div/div[2]/div/input")
        username_input.send_keys(self.email)

        next_input_button = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div/div/div/div/div[2]"\
                                                          "/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]")
        next_input_button.click()

        time.sleep(1)

        try:
            confirm_username_input = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div/div"\
                                                           "/div/div/div[2]/div[2]/div/div/div[2]/div[2]"\
                                                           "/div[1]/div/div[2]/label/div/div[2]/div/input")
            confirm_username_input.send_keys(self.username)


            next_input_button = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div"\
                                                                   "/div/div/div/div[2]/div[2]/div/div/div[2]"\
                                                                   "/div[2]/div[2]/div/div/div/button")
            next_input_button.click()

            time.sleep(1)
        except:
            pass
        finally:
            password_input = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div/div/div"\
                                                                "/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]"\
                                                                "/div/div/div[3]/div/label/div/div[2]/div[1]/input")
            password_input.send_keys(self.password)

            confirm_login_button = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div"\
                                                                      "/div/div/div/div[2]/div[2]/div/div/div[2]"\
                                                                      "/div[2]/div[2]/div/div[1]/div/div/button")
            confirm_login_button.click()

    def post_tweet(self, message):
        create_tweet_button = self.driver.find_element(By.XPATH, "//*[@id=\"react-root\"]/div/div/div[2]"\
                                                       "/header/div/div/div/div[1]/div[3]/a")
        create_tweet_button.click()

        time.sleep(.5)

        pyautogui.typewrite(message, interval=.02)

        time.sleep(.1)

        tweet_button = self.driver.find_element(By.XPATH, "//*[@id=\"layers\"]/div[2]/div/div/div/div/div"\
                                                 "/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]"\
                                                 "/div/div/div/div[2]/div[2]/div/div/div/button[2]/div")
        tweet_button.click()

    def exit(self):
        self.driver.quit()