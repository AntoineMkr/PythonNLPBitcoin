import sys, tweepy, csv, re, json, os
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
        fig2 = go.Scatter(x=args[0].index, y=args[0]['Dernier'], name="Bitcoin price")
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(fig,secondary_y=False)
    fig3.add_trace(fig2,secondary_y=True)

    fig3.update_yaxes(title_text="Bitcoin price", secondary_y=False)
    fig3.update_yaxes(title_text="Market Sentiment")
    fig3.show()

if __name__== "__main__":

    # sa = SentimentAnalysis()
    # df = pd.DataFrame()
    # df = GetSentiment("./tweets3/tweets2.csv")
    # df.to_csv('./tweets3/sentiment2.csv', index=True)

    # # print(df)

    finalDf = pd.read_csv("./tweets3/sentiment2.csv")

    # finalDf['Counter'] = finalDf.shape[1] - finalDf.apply(lambda x: x.isnull().sum(), axis='columns')
    # finalDf['Counter'] = finalDf.rolling(window=5,center=False).mean()
    # finalDf['Sentiment'] = finalDf['Sentiment'] * finalDf['Counter']
    print(finalDf)
    # finalDf['Sentiment']= finalDf['Sentiment'].replace(np.nan, 0)
    finalDf.set_index(finalDf['Date'], inplace =True)

    del finalDf['Date']
    print(finalDf['2020-01-02':].head())
    btcusd = pd.read_csv("./BTCUSD3.csv")
    btcusd.set_index(btcusd['Date'], inplace =True)

    # print(btcusd['Date'][0])
    finalDf = finalDf.rolling(window=14,center=True).mean()
    CreationChart(finalDf, btcusd['2020-01-01':])