import sys, tweepy, csv, re, json
from textblob import TextBlob
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots


from getTwitterHandles import getTwitterHandles
import pandas as pd
import numpy as np
import datetime as dt
import glob

def GetSentiment(fileName):

  # creating some variables to store info
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0

    NoOfTerms = 0
    new_df = pd.DataFrame()
    try:
        print("\n\nAnalysing tweets of " + fileName[10:-11] )
        df = pd.read_csv(fileName)
        df['created_at'] = pd.to_datetime(df['created_at'])
        # df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
        new_df['Date'] = df['created_at']

        new_df['Stmt ' + fileName[10:-11]] = np.nan

        for index, row in df.iterrows():
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            NoOfTerms +=1
            analysis = TextBlob(str(row.text))
            # print(analysis.sentiment)  # print tweet's polarity
            new_df.loc[index, 'Stmt ' + fileName[10:-11]] = analysis.sentiment.polarity 
            # polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
            

    except: 
        pass

    new_df.set_index(new_df['Date'], inplace =True)

    del new_df['Date']
    new_df = new_df.resample('D').mean()

    return new_df


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
        fig2 = go.Scatter(x=args[0]['Date'], y=args[0]['Dernier'], name="Bitcoin price")
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(fig,secondary_y=False)
    fig3.add_trace(fig2,secondary_y=True)

    fig3.update_yaxes(title_text="Bitcoin price", secondary_y=False)
    fig3.update_yaxes(title_text="Market Sentiment")
    fig3.show()

if __name__== "__main__":

    # sa = SentimentAnalysis()
    df = pd.DataFrame()
    df = GetSentiment("./tweets2/cz_binance_tweets.csv")

    for fname in glob.glob("./tweets2/*.csv"):
        if(fname != "./tweets2/cz_binance_tweets.csv"):
            df2 = GetSentiment(fname)
            if(df2.shape[0] > 100):
                if(df.shape[0] > df2.shape[0]):
                    df = df.join(df2, how = 'outer')
                else:
                    df2 = df2.join(df, how = 'outer')
                    df = df2
    
    finalDf = pd.DataFrame(index = df.index)
    finalDf['Sentiment'] = np.nan
    for index, row in df.iterrows():
        finalDf.loc[index, 'Sentiment'] = df.loc[index, :].sum(axis = 0)
    # finalDf['Counter'] = df.shape[1] - df.apply(lambda x: x.isnull().sum(), axis='columns')
    # finalDf['Sentiment'] = finalDf['Sentiment'] * finalDf['Counter']
    print(finalDf)
    finalDf['Sentiment']= finalDf['Sentiment'].replace(np.nan, 0)

    btcusd = pd.read_csv("./BTCUSD3.csv")
    print(btcusd['Date'][0])
    CreationChart(finalDf.loc[btcusd['Date'][0]:], btcusd)