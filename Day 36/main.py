from twilio.rest import Client
import os
import requests


os.environ["TWILIO_SID"] = "AC3d923a13721e99dc1d88209c45e3e500"
os.environ["TWILIO_API_AUTH"] = "ab3f957aeae20cfa4a51aa2cd8150f04"
os.environ["ALPHAVANTAGE_API_KEY"] = "P1066EOYLLKUM8YI"

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH = os.environ["TWILIO_API_AUTH"]
TWILIO_PHONE = "+12184338663"

ALPHAVANTAGE_API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]

RECEIVER_PHONE = "+639457850386"

STOCK_SYMBOL = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_PRICE_PARAMS = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_SYMBOL,
    "apikey" : ALPHAVANTAGE_API_KEY
}

NEWS_PARAMS = {
    "function" : "NEWS_SENTIMENT",
    "tickers" : STOCK_SYMBOL,
    "apikey" : ALPHAVANTAGE_API_KEY
}

def cut_string(text):
    if len(text) > 50: return text[:50] + "..."
    else: return text

def has_great_price_movement(latest, before, return_percent_diff = None):
    if not(return_percent_diff):
        return latest/before>=1.05 or latest/before<=.95
    else:
        if latest > before: return round((latest/before - latest//before) * 100, 1)
        else: return round((latest-before)/latest * 100, 1)


## Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_price_request = requests.get(url="https://www.alphavantage.co/query", params=STOCK_PRICE_PARAMS)
stock_price_data = stock_price_request.json()

closing_stock_price_latest_date_list = stock_price_data["Meta Data"]["3. Last Refreshed"].split("-")
closing_stock_price_latest_year = int(closing_stock_price_latest_date_list[0])
closing_stock_price_latest_month = int(closing_stock_price_latest_date_list[1])
closing_stock_price_latest_day = int(closing_stock_price_latest_date_list[2])

closing_stock_price_latest_date = (f"{closing_stock_price_latest_year}"\
                                   f"-{closing_stock_price_latest_month}"\
                                   f"-{closing_stock_price_latest_day}")

closing_stock_price_before_latest_year = closing_stock_price_latest_year
closing_stock_price_before_latest_month = closing_stock_price_latest_month
closing_stock_price_before_latest_day = closing_stock_price_latest_day - 1

closing_stock_price_before_latest_date = (f"{closing_stock_price_before_latest_year}"\
                                          f"-{closing_stock_price_before_latest_month}"\
                                          f"-{closing_stock_price_before_latest_day}")

closing_stock_price_latest = float(stock_price_data["Time Series (Daily)"][closing_stock_price_latest_date]["4. close"])
closing_stock_price_before_latest = float(stock_price_data["Time Series (Daily)"]\
                                    [closing_stock_price_before_latest_date]["4. close"])


## Use https://newsapi.org (Optional)
# If has great price movement, get the first 3 news pieces for the COMPANY_NAME.
if has_great_price_movement(closing_stock_price_latest, closing_stock_price_before_latest):
    news_request = requests.get(url="https://www.alphavantage.co/query", params=NEWS_PARAMS)
    news_data = news_request.json()

    news_infos = []

    for news in news_data["feed"][:3]:
        news_info = {}
        news_info["headline"] = news["title"]
        news_info["summary"] = news["summary"]
        news_info["sentiment"] = news["overall_sentiment_label"]
        news_info["source"] = news["source_domain"]
        news_infos.append(news_info)

    if closing_stock_price_latest > closing_stock_price_before_latest: message_ticker = "🔺"
    else: message_ticker = "🔻"

    percent_diff = has_great_price_movement(closing_stock_price_latest,
                                            closing_stock_price_before_latest,
                                            return_percent_diff=True)

    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    for info in news_infos:
        sentiment = info["sentiment"].title()
        heading = cut_string(info["headline"])
        brief = cut_string(info["summary"])
        source = cut_string(info["source"])

        message = f"{STOCK_SYMBOL}: {message_ticker}{percent_diff}%\n"\
        f"Headline: {heading}\n"\
        f"Brief: {brief}\n"\
        f"{sentiment}"

        sms_client = Client(TWILIO_SID, TWILIO_AUTH)
        sms = sms_client.messages.create(
            from_=TWILIO_PHONE,
            to=RECEIVER_PHONE,
            body=message
        )

        print(sms.status)

