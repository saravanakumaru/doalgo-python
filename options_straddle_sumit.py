import json
import requests
import numpy
import pandas as pd
from io import StringIO

from datetime import datetime as dt
from datetime import timedelta
import time



quote = "https://api.kite.trade/quote?i="
instruments = "https://api.kite.trade/instruments"

def get_token():
    return "enctoken r4RFELTASOcj+eUEn0k+S/8mH/tco1dLdf3HSKbDCRtP0KWuy9Piu2uJTU5qIbb1wLdUyoEroPX9PMwtGV9PJNsHFqKoIA=="

headers = { "X-Kite-Version" : "3",
            "Authorization" : 'enctoken ' + get_token()}

def qnse(smb):
    js = requests.get(quote + smb, headers=headers).json()
    df = pd.DataFrame(js['data'])
    df = df.T
    df1 = df['ohlc'].apply(pd.Series)
    df.drop(['depth', 'ohlc', 'last_quantity', 'lower_circuit_limit', 'upper_circuit_limit'], 1, inplace=True)
    df = pd.concat([df, df1], axis=1)
    return df

def lq(df1, exp):
    df1 = df1[df1.expiry == exp]
    separator = '&i='
    niftyopt = list(map(str, df1['instrument_token'].tolist()))
    nfo1 = separator.join(niftyopt[0:1000])
    df = qnse(nfo1)
    df = pd.merge(df1, df, on='instrument_token')
    df.fillna(0)
    return df

def place_order(tradingsymbol, quantity):

    url = "https://kite.zerodha.com/oms/orders/regular"

    payload = 'exchange=NFO&tradingsymbol={}&transaction_type=SELL&order_type=MARKET&quantity={}&price=0&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price=0&squareoff=0&stoploss=0&trailing_stoploss=0&variety=regular&user_id=<YOUR-USER-ID>'.format(tradingsymbol, quantity)
    print(payload)
    headers = {
      'content-type': 'application/x-www-form-urlencoded',
      'authorization': 'enctoken ' + get_token(),
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    response = response.json()
    print(response, "responsee")

def straddle(df, near_price, name, qty):
    # print(df.head())
    ddf = df[(df.last_price < near_price) & (df.name == name)]
    # ddf = ddf.sort_values('volume', ascending=False)
    dd = ddf[['tradingsymbol', 'instrument_type', 'last_price', 'volume', 'strike']]

    highest_CE = dd[dd['instrument_type'] == 'CE']['last_price'].max()
    lowest_PE = dd[dd['instrument_type'] == 'PE']['last_price'].max()

    CE_sell = dd[dd['last_price'] == highest_CE].max()
    PE_sell = dd[dd['last_price'] == lowest_PE].max()

    CE_sell = CE_sell.get(key='tradingsymbol')
    PE_sell = PE_sell.get(key='tradingsymbol')
    print(dd)
    print(name + "=CE_sell", CE_sell, name + "=PE_sell", PE_sell)
    place_order(CE_sell, qty)
    place_order(PE_sell, qty)

def lambda_handler(event, context):

    inst = requests.get(instruments + '/NFO', headers=headers).text
    df = pd.read_csv(StringIO(inst))
    df1 = df[df.segment == 'NFO-OPT']

    
    df10 = df1[(df1.name.isin(['BANKNIFTY', 'NIFTY']))]
    df10 = df10[['instrument_token', 'tradingsymbol', 'expiry', 'strike', 'instrument_type', 'name']]
    exp = df1.expiry.unique()

    df = lq(df10, '2021-02-11')

    straddle(df, 50,'BANKNIFTY', 50)
    straddle(df, 20, 'NIFTY', 150)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }





