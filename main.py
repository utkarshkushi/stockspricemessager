import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCKS = os.environ.get('STOCKS_API')
API_KEY_NEWS = os.environ.get('NEWS_API')
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
twilio_number = os.environ.get("TWILIO_NUMBER")
my_number = os.environ.get("MY_NUMBER")

stocks_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCKS
}
response = requests.get(url="https://www.alphavantage.co/query", params=stocks_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

closing_price_list = []
day = 0
for date in data:
    day += 1
    if day <= 2:
        close_price = float(data[date]["4. close"])
        closing_price_list.append(close_price)


percentage_change = (closing_price_list[0] - closing_price_list[1])/closing_price_list[0] * 100
print(percentage_change)
if percentage_change < 0:
    percentage_change = f"{COMPANY_NAME}🔻 {abs(round(percentage_change, 3))}%"
else:
    percentage_change = f"{COMPANY_NAME}🔺 {abs(round(percentage_change, 3))}%"

news_params = {
    "q": "tesla",
    "sortBy": "popularity",
    "apikey": API_KEY_NEWS
}
news_response = requests.get("https://newsapi.org/v2/everything", params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
print(news_data["articles"][0]["title"])

client_2 = Client(account_sid, auth_token)

message = client_2.messages \
    .create(
    body=f"{percentage_change}\n  Headline: {news_data['articles'][1]['title']}\n "
         f"Brief: {news_data['articles'][1]['description']} ",
    from_=twilio_number,
    to=my_number
)
print(message.status)

client_3 = Client(account_sid, auth_token)

message = client_3.messages \
    .create(
    body=f"{percentage_change}\n 1. Headline: {news_data['articles'][2]['title']}\n "
         f"Brief: {news_data['articles'][2]['description']} ",
    from_=twilio_number,
    to=my_number
)
print(message.status)

