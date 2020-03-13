from bitfinex import WssClient, ClientV2, ClientV1
import datetime
from datetime import datetime as datetime2
import time
import pandas as pd


# Define query parameters
PAIR = 'BNBUSD' # Currency pair of interest
BINSIZE = '5m' # This will return minute data
LIMIT = 10000    # We want the maximum of 1000 data points 
APIKEY = 'Lm4QXQhVHUH24UeY2Ym4ih5NnpYYk3TtG8V4hb9jJiC' #your apikey of bitfinex
APISECRET = 'Bs7bjJUUUl4byEMUFdApx7tbzSd2pSFEA7YE2mcOpQe' # your secret key of bitfinex
TIMESTEP = 90000000 # Set step size



def save_data(symbol,pair_data):
    """
    Parameters: 
        * name (str) - Name of file
        * symbol (str) - Symbol for name 
        * pair_data - List of data 

    This function is to save the information returned by "get_data". To save, Pandas is used, modifying the received list and converting it into a DataFrame
    """
    
    if pair_data:
        # Create pandas data frame and clean/format data
        names = ['time', 'open', 'close', 'high', 'low', 'volume']
        df = pd.DataFrame(pair_data, columns=names)
        df.drop_duplicates(inplace=True)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        df.sort_index(inplace=True)
        df.to_csv('./recolect/{}.csv'.format(symbol))
# Connection BitFinex
bfx_client = ClientV2(APIKEY,APISECRET)


# Define the start date 
t_start = datetime.datetime(2014, 1, 1)
start = time.mktime(t_start.timetuple()) * 1000

# Define the end date
t_stop = datetime.datetime(2020, 2, 29)
stop = time.mktime(t_stop.timetuple()) * 1000

symbol = 'tBTCUSD'

candles = bfx_client.candles(timeframe='5m',symbol=symbol,section='hist',limit=LIMIT,start=start,end=stop,sort=1)

save_data(symbol,candles)