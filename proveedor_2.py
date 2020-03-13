import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import sys, os

def CryptoData(symbol, frequency):
    try:
        #Params: String symbol, int frequency = 300,900,1800,7200,14400,86400
        #Returns: df from first available date
        response = requests.get('https://poloniex.com/public?command=returnChartData&currencyPair='+symbol+'&end=9999999999&period='+str(frequency)+'&start=0&resolution=auto')
        data = json.loads(response.text)
        stockprices = pd.DataFrame(data)
        stockprices['date'] = pd.to_datetime(stockprices['date'],unit='s')
        stockprices.set_index('date',inplace=True)
        stockprices['20d'] = stockprices['close'].rolling(20).mean()
        stockprices['250d'] = stockprices['close'].rolling(250).mean()
    
        stockprices[['close','20d','250d']].plot(figsize=(10,4))
        plt.grid(True)
        plt.title(symbol + ' Moving Averages')
        plt.axis('tight')
        plt.ylabel('Price')
        return stockprices
    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type,exc_obj, fname, exc_tb.tb_lineno,err)

df = CryptoData(symbol = 'BTC_LTC', frequency = 300)
print(df.head())