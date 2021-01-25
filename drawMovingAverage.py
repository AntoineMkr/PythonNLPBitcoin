import sys, tweepy, csv, re, json, os
from textblob import TextBlob
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import datetime as dt
import glob


def GetSentiment(fileName, fileout):

  # creating some variables to store info
    NoOfTerms = 0
    new_df = pd.DataFrame()
    try:
        # print("\n\nAnalysing tweets of " + fileName[10:-11] )
        print("Analysing tweets...")
        df = pd.read_csv(fileName)
        
        df['created_at'] = pd.to_datetime(df['created_at'])
        # df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
        new_df['Date'] = df['created_at']

        for index, row in df.iterrows():
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            NoOfTerms +=1
            os.system('clear')
            print(str(NoOfTerms) + "/" + str(df.shape[0]))
            analysis = TextBlob(str(row.Text))
            # print(analysis.sentiment)  # print tweet's polarity
            new_df.loc[index, 'Sentiment'] = analysis.sentiment.polarity 
            # polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
            

    except: 
        pass

    new_df.set_index(new_df['Date'], inplace =True)

    del new_df['Date']
    new_df = new_df.resample('D').sum()
    
    new_df.to_csv(fileout)


# function to calculate percentage
def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def CreationChart(dataframe, *args):

    # fig = go.Figure(data=go.Scatter(x=dataframe.index, y=dataframe['Sentiment'], name="Sentiment"))
    # if(len(args) != 0):
    #     fig2 = go.Figure(data=go.Scatter(x=args[0]['Date'], y=args[0]['Dernier'], name="Bitcoin price"))
    fig = go.Scatter(x=dataframe.index, y=dataframe['Sentiment'], name="Sentiment")
    if(len(args) != 0):
        fig2 = go.Scatter(x=args[0].index, y=args[0]['Dernier'], name="Bitcoin price")
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(fig,secondary_y=False)
    fig3.add_trace(fig2,secondary_y=True)

    fig3.update_yaxes(title_text="Bitcoin price", secondary_y=False)
    fig3.update_yaxes(title_text="Market Sentiment")
    fig3.show()

if __name__== "__main__":

    
    # GetSentiment("./mainData/hashtag.csv", "./tweets3/sentimentHashtag.csv")
    
    # create sentiment dataframe
    df1 = pd.read_csv("./mainData/sentimentHashtag.csv")
    # setting date as index
    df1.set_index(df1['Date'], inplace =True)
    del df1['Date']

    # Create btcusd dataframe
    btcusd = pd.read_csv("./BTC_price/BTCUSDClean.csv")
    btcusd.set_index(btcusd['Date'], inplace =True)

    # compute moving average
    df1 = df1.rolling(window=30,center=True).mean()

    #Display chart
    CreationChart(df1, btcusd['2020-01-01':])
