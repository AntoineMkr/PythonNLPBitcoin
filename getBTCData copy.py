#import fbprophet

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import csv

def ModifCsv(csvFile):
    btcusd = pd.read_csv(csvFile)

    btcusd['Date'] = pd.to_datetime(btcusd['Date'])
    btcusd.sort_values(by=['Date'], inplace = True)
    btcusd = btcusd[['Date', 'Close']]
    # btcusd['Close'] = btcusd['Close'].str.replace(".", "")
    btcusd['Close'] = btcusd['Close'].astype('float')
    btcusd['Close'] = round(btcusd['Close'],2)
    btcusd.rename(columns={"Close": "Dernier"})
    print(btcusd.head())
    btcusd.to_csv(r'./BTC_price/BTCUSDClean2.csv', index = False, header = True)


def CreationChart(btcusd):
    fig = go.Figure([go.Scatter(x=btcusd['Date'], y=btcusd['Dernier'])])
    fig.show()
  

if __name__ == "__main__":
    btcusdfile = "./BTC_price/BTC-USD.csv"
    ModifCsv(btcusdfile) 
    # btcusd = pd.read_csv(btcusdfile)
    # CreationChart(btcusd)
