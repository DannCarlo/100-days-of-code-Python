import os
import time
from speedtest import SpeedTest
from twitter_handle import TwitterHandle

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")

PROMISED_DOWNLOAD_SPEED = 100
PROMISED_UPLOAD_SPEED = 100

# Get network speed results
speedtest = SpeedTest()

download_speed = speedtest.download_speed
upload_speed = speedtest.upload_speed

speedtest.exit()

# If network speed is slower than promised by provider, post in Twitter
if download_speed<PROMISED_DOWNLOAD_SPEED or upload_speed<PROMISED_UPLOAD_SPEED:
    pldt_message = (f"""@PLDT_CARES promised dl speed: {PROMISED_DOWNLOAD_SPEED}mbps, what I got: {download_speed}mbps
PLDT, Anuna??""")

    twitter = TwitterHandle(USERNAME, EMAIL, PASSWORD)
    twitter.login_account()

    time.sleep(5)

    twitter.post_tweet(pldt_message)
    twitter.exit()

