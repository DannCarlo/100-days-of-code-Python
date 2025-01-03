import requests
import datetime as dt

USER_TOKEN = "----~~~~"
USERNAME = "trialuser"

GRAPH_ID = "code100"

PIXELA_CREATE_USER_URL = "https://pixe.la/v1/users"
PIXELA_CREATE_GRAPH_URL = f"{PIXELA_CREATE_USER_URL}/{USERNAME}/graphs"
PIXEL_URL = f"{PIXELA_CREATE_GRAPH_URL}/{GRAPH_ID}"

CREATE_USER_DATA = {
    "token" : USER_TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes",
    "thanksCode" : "thanks-code"
}

TOKEN_HEADER_DATA = {
    "X-USER-TOKEN" : USER_TOKEN
}

CREATE_GRAPH_DATA = {
    "id" : GRAPH_ID,
    "name" : "100 days of code",
    "unit" : "study hours",
    "type" : "int",
    "color" : "shibafu",
    "timezone" : "Asia/Manila"
}

date_todaytime = dt.datetime.now()
date_today = f"{date_todaytime.year}{date_todaytime.month}{date_todaytime.day}"

pixel_data = {
    "date" : date_today
}

create_user_request = requests.post(url= PIXELA_CREATE_USER_URL, json=CREATE_USER_DATA)
create_user_data = create_user_request.json()

create_graph_request = requests.post(url=PIXELA_CREATE_GRAPH_URL, json=CREATE_GRAPH_DATA, headers=TOKEN_HEADER_DATA)

pixel_action = input("What to do with your pixel? 'p' for post, 'u' for update, 'd' for delete ")

if pixel_action == "p":
    quantity = input("How long did you study today? ")

else:
    PIXEL_URL = f"{PIXEL_URL}/{date_today}"

    if pixel_action == "u":
        pixel_data.pop("date")
        quantity = input("How long did you study today? ")
    else: quantity = None

pixel_data["quantity"] = quantity

is_request_fail = True

while is_request_fail:
    if pixel_action == "p":
        pixel_request = requests.post(url=PIXEL_URL, json=pixel_data, headers=TOKEN_HEADER_DATA)
    elif pixel_action == "u":
        pixel_request = requests.put(url=PIXEL_URL, json=pixel_data, headers=TOKEN_HEADER_DATA)
    else:
        pixel_request = requests.delete(url=PIXEL_URL, headers=TOKEN_HEADER_DATA)
    pixel_data_from_req = pixel_request.json()

    if pixel_data_from_req["isSuccess"]: is_request_fail = False
