##################### Extra Hard Starting Project ######################
import pandas as pd
import datetime as dt
import random
import smtplib

SENDER_EMAIL = "email@yahoo.com"
SENDER_PW = ""

SMTP_HOST = "smtp.mail.yahoo.com"


# Get birthdays.csv
birthdays_dataframe = pd.read_csv("birthdays.csv")

date_now = dt.date.today()


# Check if today matches a birthday in the birthdays.csv
for key, row in (birthdays_dataframe[(birthdays_dataframe["month"] == date_now.month)
                & (birthdays_dataframe["day"] == date_now.day)].iterrows()):
    name = row["name"]
    email = row["email"]

    # Pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as letter_file:
        letter_template = "".join(letter_file.readlines())
        letter_template = letter_template.replace("[NAME]", name)

    # Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP(SMTP_HOST, port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=SENDER_PW)
        connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=email, msg=f"Subject: Happy Birthday!\n\n{letter_template}")





