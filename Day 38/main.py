import os
import requests
import datetime as dt

os.environ["NUTRITIONIX_AID"] = "e8d034ca"
os.environ["NUTRITIONIX_APP_KEY"] = "175df32035ab2f3782012c8b5debc649"

os.environ["SHEETY_AUTH"] = "Bearer sdklsdflsdlkfgkldfjlghjgflhkfghzzxcvcvxcv"

NUTRITIONIX_AID = os.environ.get("NUTRITIONIX_AID")
NUTRITIONIX_APP_KEY = os.environ.get("NUTRITIONIX_APP_KEY")

SHEETY_AUTH = os.environ.get("SHEETY_AUTH")

NUTRITIONIX_EXERCISE_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_POST_URL = "https://api.sheety.co/9f9e57b04371f4dfdc63dd0e26bbec41/copyOfMyWorkoutsPythonExercise/workouts"

SHEETY_HEADER_DATA = {
    "Authorization" : SHEETY_AUTH
}

NUTRITIONIX_HEADER_DATA = {
    "x-app-id" : NUTRITIONIX_AID,
    "x-app-key" : NUTRITIONIX_APP_KEY
}

datetime_now = dt.datetime.now()
time_now = datetime_now.strftime("%X")
date_now = datetime_now.strftime("%d/%m/%Y")

query = input("Tell me with exercise you did today? ")

query_post_data = {
    "query" : query
}

nutritionix_request = requests.post(url=NUTRITIONIX_EXERCISE_URL, json=query_post_data, headers=NUTRITIONIX_HEADER_DATA)
nutritionix_data = nutritionix_request.json()

for data in nutritionix_data["exercises"]:
    post_data = {
        "workout" : {}
    }

    print(data["name"].title())

    post_data["workout"]["date"] = date_now
    post_data["workout"]["time"] = time_now
    post_data["workout"]["exercise"] = data["name"].title()
    post_data["workout"]["duration"] = data["duration_min"]
    post_data["workout"]["calories"] = data["nf_calories"]

    sheety_request = requests.post(url=SHEETY_POST_URL, json=post_data, headers=SHEETY_HEADER_DATA)


