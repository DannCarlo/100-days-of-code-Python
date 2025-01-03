import smtplib
import random

SENDER_EMAIL = "email@yahoo.com"
SENDER_PW = ""

RECEIVER_EMAIL = "email@gmail.com"

SMTP_HOST = "smtp.mail.yahoo.com"

with open("quote.txt", encoding="utf8") as file:
    quotes_list = file.readlines()
    quote = random.choice(quotes_list).strip()

quote = quote.encode("UTF-8")

with smtplib.SMTP(SMTP_HOST, port=587) as connection:
    connection.starttls()
    connection.login(user=SENDER_EMAIL, password=SENDER_PW)
    connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECEIVER_EMAIL, msg=f"Subject: Quote of the day\n\n{quote}")