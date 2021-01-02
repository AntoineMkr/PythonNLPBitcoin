## Bitcoin Sentiment analysis

You need a Twitter dev accounts to have a twitter_credentials.json

### Steps:
1 ) run getTweets.py
``` 
mkdir tweets2 
python3 getTweets.py
```

2) OPTIONAL -- get BTC historical data

You can directly use the dataset of the repo.
I initially downloaded the data from the site "investing.com"
I then had to clean this data set, the code is in getBTCData.py
```
python3 getBTCData.py
```
you might have to modify the path of the file you downloaded from internet in the main section of getBTCData.py

3) run Test1.py


The file getTwitterHandles.py allows me the scrap the data fromm the website https://cryptoweekly.co/100/ so that I can get the top 100 crypto influencers. They potentially have a bigger influence on the price.

preprocessingTweets.py contains functions that I use to clean the tweets. By "clean" I mean removing emojis, strange characters, links...