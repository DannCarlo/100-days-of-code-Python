import requests
from bs4 import BeautifulSoup

AMAZON_URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

HEADERS = {
    "User-agent" : ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"),
    "Accept" : "text/html",
    "sec-ch-ua" : "Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24"
}

amazon_request = requests.get(url=AMAZON_URL, headers=HEADERS)
amazon_html = amazon_request.text

soup = BeautifulSoup(markup=amazon_html, features="html.parser")

price_element = soup.select(selector="#ppd #centerCol .a-section > .aok-offscreen")[0]
price = float(price_element.getText().strip()[1:])

if price < 100:
    print("Buy now.")