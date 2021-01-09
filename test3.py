import sys, tweepy, csv, re, json, os
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import reuters
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots


from getTwitterHandles import getTwitterHandles
import pandas as pd
import numpy as np
import datetime as dt
import glob


# new_corpus = 

train = [
    ('I am bullish on bitcoin', 'pos'),
    ('It is pumping hard!', 'pos'),
    ('You must buy bitcoin', 'pos'),
    ('This is my best work.', 'pos'),
    ("What an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg')
]
test = [
    ('The beer was good.', 'pos'),
    ('I do not enjoy my job', 'neg'),
    ("I ain't feeling dandy today.", 'neg'),
    ("I feel amazing!", 'pos'),
    ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]

cl = NaiveBayesClassifier(train)

# Classify some text
print(cl.classify("This stock is profitable."))  # "pos"
print(cl.classify("I don't like their pizza."))   # "neg"

# Classify a TextBlob
blob = TextBlob("I am bullish about bitcoin", classifier=cl)
print(blob)
print(blob.classify())

for sentence in blob.sentences:
    print(sentence)
    print(sentence.classify())



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

# if __name__== "__main__":

#     # sa = SentimentAnalysis()
#     # df = pd.DataFrame()
#     # df = GetSentiment("./tweets3/tweets.csv")
#     # df.to_csv('./tweets3/sentiment.csv', index=True)

#     # print(df)

#     finalDf = pd.read_csv("./tweets3/sentiment.csv")

#     # finalDf['Counter'] = df.shape[1] - df.apply(lambda x: x.isnull().sum(), axis='columns')
#     # finalDf['Sentiment'] = finalDf['Sentiment'] * finalDf['Counter']
#     print(finalDf)
#     # finalDf['Sentiment']= finalDf['Sentiment'].replace(np.nan, 0)
#     finalDf.set_index(finalDf['Date'], inplace =True)

#     del finalDf['Date']
#     print(finalDf['2020-01-02':].head())
#     btcusd = pd.read_csv("./BTCUSD3.csv")
#     btcusd.set_index(btcusd['Date'], inplace =True)

#     print(btcusd['Date'][0])
#     CreationChart(finalDf, btcusd['2020-01-01':])