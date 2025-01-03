from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
import requests

OPENWEATHER_PARAMS = {
    "lat" : 0,
    "lon" : 0,
    "cnt" : 0,
    "appid" : ""
}

TWILIO_SID = ""
TWILIO_AUTH = ""
TWILIO_PHONE = ""

weather_request = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=OPENWEATHER_PARAMS)
weather_data = weather_request.json()

for weather in weather_data["list"]:
    if weather["weather"][0]["id"] > 700:

        message = f""

        phone_num = ""

        try:
            sms_client = Client(TWILIO_SID, TWILIO_AUTH)
            sms = sms_client.messages.create(
                from_=TWILIO_PHONE,
                to=phone_num,
                body=message
            )
        except TwilioRestException:
            pass

        break


