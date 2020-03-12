# We import the necessary modules for the correct execution of the code
import time
import datetime
from datetime import datetime as datetime2
import pandas as pd
from tqdm import tqdm
import sys
import json
from bitfinex import WssClient, ClientV2, ClientV1

# Define query parameters
PAIR = 'BNBUSD' # Currency pair of interest
BINSIZE = '5m' # This will return minute data
LIMIT = 1000    # We want the maximum of 1000 data points 
APIKEY = 'Lm4QXQhVHUH24UeY2Ym4ih5NnpYYk3TtG8V4hb9jJiC' #your apikey of bitfinex
APISECRET = 'Bs7bjJUUUl4byEMUFdApx7tbzSd2pSFEA7YE2mcOpQe' # your secret key of bitfinex
TIMESTEP = 90000000 # Set step size

# Connection BitFinex
bfx_client = ClientV2(APIKEY,APISECRET)



def save_data(name,symbol,pair_data):
    """
    Parameters: 
        * name (str) - Name of file
        * symbol (str) - Symbol for name 
        * pair_data - List of data 

    This function is to save the information returned by "get_data". To save, Pandas is used, modifying the received list and converting it into a DataFrame
    """
    
    if pair_data:
        name = name.replace(' ','_')
        # Create pandas data frame and clean/format data
        names = ['time', 'open', 'close', 'high', 'low', 'volume']
        df = pd.DataFrame(pair_data, columns=names)
        df.drop_duplicates(inplace=True)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        df.sort_index(inplace=True)
        df.to_csv('./recolect/{}_{}.csv'.format(name,symbol))



def generate_rango(start,end,step_days):
    """
    Parameters: 
        * start (datetime) - start date
        * end (datetime) - end date
        * step_days (int) - number of days to consider it an episode, for example: step_days = 365 (it means that each episode will have 365 days)

    create range of date with start date and end"""
    rango = []
    dias_totales = (end - start).days
    
    global_count = 0
    count = 0
    aux = 0
    dias = step_days
    secon_list = []
    obj = {}
    
    for days in range(dias_totales + 1):
        try:
            _date = start + datetime.timedelta(days=days) 
        
            
            if aux < dias:
                secon_list.append(_date.strftime("%Y-%m-%d %H:%M:%S"))
                aux = aux + 1

            elif aux >= dias:
                obj['time{}'.format(count)] = secon_list[:]
                secon_list.clear()
                aux = 0
                count = count + 1

        except Exception as err:
            print(err)

    rango.append(obj)        
    return (rango)




def get_data(altcoin, timeframe,start, end):
    altcoin_list = [(item.splitlines()[0]).split(',') for item in altcoin ]
    obj = generate_rango(start,end,365)
    retorno_data = []
    no_ = []
    for item in tqdm(altcoin_list,ascii=True,desc='List altcoin'):
        symbol = 't{}USD'.format(item[1])
        validate_symbol = bfx_client.tickers([symbol])
        time.sleep(1)
        if validate_symbol:
            for key in tqdm(obj[0].keys(),ascii=True,desc=symbol):
                _min = (datetime2.strptime(min(obj[0][key]),"%Y-%m-%d %H:%M:%S"))
                _max = (datetime2.strptime(max(obj[0][key]),"%Y-%m-%d %H:%M:%S"))
                start = time.mktime(_min.timetuple()) * 1000
                stop = time.mktime(_max.timetuple()) * 1000
                candles = bfx_client.candles(timeframe=timeframe,symbol=symbol,section='hist',limit=LIMIT,start=start,end=stop,sort=1)
                retorno_data.extend(candles)
                time.sleep(1)
        else:
            no_.append(symbol)
        save_data(item[0],symbol, retorno_data)
        retorno_data.clear()
    
    print(no_)

            

# Define the start date 
t_start = datetime.datetime(2014, 1, 1)

# Define the end date
t_stop = datetime.datetime(2020, 2, 29)
stop = time.mktime(t_stop.timetuple()) * 1000

with open('./altcoin.txt','r') as altcoin:
    altcoin = altcoin.readlines()

get_data(altcoin,'5m',t_start,t_stop)
