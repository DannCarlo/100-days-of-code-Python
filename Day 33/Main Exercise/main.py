import requests
import smtplib
from datetime import datetime

SMTP_HOST = ""
SMTP_PORT = 587

EMAIL = ""
PASSWORD = ""

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# If the ISS is close to my current position and my position is within +5 or -5 degrees of the ISS position.
if iss_latitude-5<=MY_LAT<=iss_latitude+5 and iss_longitude-5<=MY_LONG<=iss_longitude+5:
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")
    sunset = data["results"]["sunset"].split("T")[1].split(":")
    sunset_hour = int(sunset[0])
    sunset_min = int(sunset[1])

    time_now = datetime.now()

    hour_now = time_now.hour
    min_now = time_now.minute

    # If it is currently dark
    if hour_now>sunset_hour or (hour_now==sunset_hour and min_now>=sunset_min):

        # Then send me an email to tell me to look up.
        with smtplib.SMTP(SMTP_HOST, port=SMTP_PORT) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f"Subject:Look up\n\nThe ISS is above you,"\
                                                                     f"your coordinates are {MY_LONG, MY_LAT}"\
                                                                     f"and ISS coordinates are {iss_longitude, iss_latitude}")
    else:
        print(iss_latitude, iss_longitude)



