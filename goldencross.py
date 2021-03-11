import pandas as pd
import bybit
import time

# Every "interval" sec, the bot collect BTCUSD data and determin whether take position or not. 
interval = 5

# Amount of position(USD).
quantity = 100

# In many cases, short-term-moving-average uses 25 and long-term-moving-average uses 75.
short_sma_duration = 25
long_sma_duration = 75

api_key=input("Please input your api key of bybit.")
api_secret=input("Please input your api secret key of bybit.")


client = bybit.bybit(test=True, api_key=api_key, api_secret=api_secret)

# This bot do nothing until collecting 100 sample BTCUSD data. 
def price_data_collecting(samples=100):
    prices = []
    for _ in range(samples):
        last_price = client.Market.Market_symbolInfo(symbol="BTCUSD").result()[0]["result"][0]["last_price"]
        prices.append(last_price)
        time.sleep(interval)
        return prices

print("From now, This program collects price data (for 5*100=500secs default). Nothing will be displayed during that time.")
BTCUSD_initial_data = price_data_collecting()

# set the data as pandas dataframe.
df = pd.DataFrame()
df["BTCUSD"] = BTCUSD_initial_data

while True:
    # latest price.
    last_price = client.Market.Market_symbolInfo().result()[0]["result"][0]["last_price"]
    df=df.append({'BTCUSD': last_price,}, ignore_index=True)

    # calc moving averages.
    df["short_sma"]=df["BTCUSD"].rolling(short_sma_duration).mean()
    df["long_sma"]=df["BTCUSD"].rolling(long_sma_duration).mean()

    # golden cross.
    if df["short_sma"].iloc[-1]>df["long_sma"].iloc[-1] and df["short_sma"].iloc[-2]<df["long_sma"].iloc[-2]:
        print("Take long position.")
        print(client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Market",qty=quantity,time_in_force="GoodTillCancel").result())

    # death cross.
    elif df["short_sma"].iloc[-1]<df["long_sma"].iloc[-1] and df["short_sma"].iloc[-2]>df["long_sma"].iloc[-2]:
        print("Take short position.")
        print(client.Order.Order_new(side="Sell",symbol="BTCUSD",order_type="Market",qty=quantity,time_in_force="GoodTillCancel").result())

    else:
        print("No crosses. The bot don't anything.")

    # delete initial row.
    df=df.drop(df.index[0])

    time.sleep(interval)
    
    
    
# Cryptocurrency algorithm trading tutorial. Trade automatically using Python codes.

