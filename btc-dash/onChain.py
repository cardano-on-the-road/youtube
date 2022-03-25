import json
import requests
import pandas as pd


# insert your API key here
API_KEY = ''

# make API request



class OnChain:
    def __init__(self,  api_key):
        self.api_key=api_key
        
    def download_hashrate(self):
        res = requests.get('https://api.glassnode.com/v1/metrics/mining/hash_rate_mean',
            params={'a': 'BTC', 'api_key': API_KEY})

        data = res.json()
        df = pd.DataFrame.from_dict(data)
        df['Date'] = pd.to_datetime(df['t'], unit='s', yearfirst=True)
        df['hashpower'] = df['v'].astype('float')
        df = df[['hashpower', 'Date']]
        df.set_index('Date', inplace=True)
        self.hashrate=df
        
    def plot_hashrate(self):
        pass
    
    def plot_wallet100(self):
        pass