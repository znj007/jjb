import pandas as pd
import pyupbit
import datetime
import requests
import pandas as pd
import time
import webbrowser
import numpy as np

access = "  "
secret = "  "


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

a = 1

while True:
    try:
        url = "https://api.upbit.com/v1/candles/minutes/5"
    
        querystring = {"market":"KRW-ETH","count":"100"}
    
        response = requests.request("GET", url, params=querystring)
    
        data = response.json()
    
        df = pd.DataFrame(data)
    
        df=df['trade_price'].iloc[::-1]
    

    
        ma4 = df.rolling(window=4).mean()
        ma15 = df.rolling(window=15).mean()
    
        test1=ma4.iloc[-2]-ma15.iloc[-2]
        test2=ma4.iloc[-1]-ma15.iloc[-1]
    
        call='해당없음'
    
        if test1>0 and test2<0:
           call='데드크로스' 
           eth = get_balance("ETH")
           if eth > 0.00008:
              upbit.sell_market_order("KRW-ETH", eth*0.9995)
        
        if test1<0 and test2>0:
           call='골든크로스'  
           krw = get_balance("KRW")
           if krw > 5000:
              upbit.buy_market_order("KRW-ETH", krw*0.9995)

    
        time.sleep(1)

    except Exception as e:
           print(e)
           time.sleep(1)
