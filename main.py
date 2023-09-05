## Assuming you're interested in the Tesla stock and wanna get some news alerts
## when there is a certain % change of stock price movement.
## Using AlphaVantage API to get stock price data
## Using NewsAPI to get the news about the company
## Using Twilio API to send an SMS to yourself

import requests
from twilio.rest import Client

#Put your own API keys and account details below
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
#stock_api_key = "YOUR_API"
#news_api_key = "YOUR_API"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
#twilio_phone = "YOUR_TWILIO_PHONE"
#my_phone = "YOUR_PHONE"
#TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_ID"
#TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"


## Get the stock price - Use https://www.alphavantage.co/documentation/#daily

stock_paramas = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}

r = requests.get(url=STOCK_ENDPOINT, params=stock_paramas)
data = r.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_date = data_list[0]
yesterday_close = yesterday_date["4. close"]
print(yesterday_close)

day_before_yesterday_data = data_list[1]
day_before_yesterday_close = day_before_yesterday_data["4. close"]

## Get the stock price difference
diff = float(yesterday_close) - float(day_before_yesterday_close)
up_down = None
if diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(diff / float(yesterday_close) * 100, 2)

# Trigger the news alert, use any percentage as you like
if abs(diff_percent) > 0.4:
    print("Get News")

## The news API: https://newsapi.org/
## Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    news_params = {
        "apiKey": news_api_key,
        "q": COMPANY_NAME,
        "searchIn": "title",
    }

    news_r = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_r.json()["articles"]

## Use twilio.com/docs/sms/quickstart/python
##to send a separate message with each article's title and description to your phone number.
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles_list = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles_list:
        message = client.messages \
            .create(
            body=article,
            from_=twilio_phone,
            to=my_phone,
        )

        print(message.sid)

