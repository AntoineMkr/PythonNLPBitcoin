'''
format_tweets.py
Includes methods for processing raw tweet data
Created by Miles Luders
'''
from string import ascii_lowercase
from nltk.corpus import words as english_words
from nltk.tag import pos_tag
import re, string
import preprocessor as p

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def process_tweets(tweet):
    
    # Remove links
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    
    # Remove mentions and hashtag
    tweet = re.sub(r'\@\w+|\#','', tweet)
    
    # Tokenize the words
    tokenized = word_tokenize(tweet)

    # Remove the stop words
    tokenized = [token for token in tokenized if token not in stopwords.words("english")] 

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokenized = [lemmatizer.lemmatize(token, pos='a') for token in tokenized]

    # Remove non-alphabetic characters and keep the words contains three or more letters
    tokenized = [token for token in tokenized if token.isalpha() and len(token)>2]
    
    return tokenized


def format_syntax(text):
    a = convert_to_lowercase(text)
    b = remove_non_alpha_chars(a)
    c = remove_excess_whitespace(b)
    return c
    

def format_semantic(text):
    english = set(w.lower() for w in english_words.words())
    stop = set(w.lower() for w in stopwords.words())
    a = remove_non_english_words(text, english)
    b = remove_stopwords(a, stop)
    
    return b

def remove_noise(txt):

    return p.clean(txt.replace(",", "")).lower()


if __name__ == "__main__":
    mot = "If you like Doge, https://t.co/VC3ISpgC2z"
    # print(" ".join(remove_noise(mot)))
    print(remove_noise(mot))