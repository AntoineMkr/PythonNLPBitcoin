#import fbprophet

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import csv

def ModifCsv(csvFile):
    btcusd = pd.read_csv(csvFile)

    btcusd['Date'] = pd.to_datetime(btcusd['Date'], format = '%d/%m/%Y')
    btcusd.sort_values(by=['Date'], inplace = True)
    btcusd = btcusd[['Date', 'Dernier']]
    btcusd['Dernier'] = btcusd['Dernier'].str.replace(".", "")
    btcusd['Dernier'] = btcusd['Dernier'].str.replace(",", ".").astype('float')
    print(btcusd.head())
    btcusd.to_csv(r'./BTCUSD3.csv', index = False, header = True)


def CreationChart(btcusd):
    fig = go.Figure([go.Scatter(x=btcusd['Date'], y=btcusd['Dernier'])])
    fig.show()
  

if __name__ == "__main__":
    btcusdfile = "./BTCUSD3.csv"
    # ModifCsv(btcusdfile) 
    btcusd = pd.read_csv(btcusdfile)
    CreationChart(btcusd)
