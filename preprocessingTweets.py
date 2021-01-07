'''
format_tweets.py
Includes methods for processing raw tweet data
Created by Miles Luders
'''
from string import ascii_lowercase
from nltk.corpus import words as english_words, stopwords
from nltk.tag import pos_tag
import re, string
import preprocessor as p

def remove_excess_whitespace(text):
    return ' '.join(text.split())
    

def convert_to_lowercase(text):
    return text.lower()
    

def remove_non_alpha_chars(text):
    T = list(text)
    i = 0
    while i < len(T):
        if T[i] not in ascii_lowercase and T[i] != ' ':
            del T[i]
        else:
            i += 1
    
    return ''.join(T)


def format_syntax(text):
    a = convert_to_lowercase(text)
    b = remove_non_alpha_chars(a)
    c = remove_excess_whitespace(b)
    return c
    

def remove_non_english_words(text, english):
    T = text.split(' ') # ["hello", "world"]
    
    i = 0
    while i < len(T):
        if T[i] not in english:
            del T[i]
        else:
            i += 1
            
    return ' '.join(T)


def remove_stopwords(text, stop):
    T = text.split(' ')
    
    i = 0
    while i < len(T):
        if T[i] in stop:
            del T[i]
        else:
            i += 1
    
    return ' '.join(T)


def format_semantic(text):
    english = set(w.lower() for w in english_words.words())
    stop = set(w.lower() for w in stopwords.words())
    a = remove_non_english_words(text, english)
    b = remove_stopwords(a, stop)
    
    return b

def remove_noise(txt):

    # cleaned_tokens = []
    # return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split()).lower()
    return p.clean(txt.replace(",", "")).lower()

    # for token in (tweet_text.split(" ")):
    #     token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
    # #                    '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
    # #     token = re.sub("(@[A-Za-z0-9_]+)","", token)

    # #     token = re.sub("https","",token)

    # #     if len(token) > 0 and token not in string.punctuation:
    #         cleaned_tokens.append(token.lower())    
    
    # return cleaned_tokens

if __name__ == "__main__":
    mot = "If you like Doge, https://t.co/VC3ISpgC2z"
    # print(" ".join(remove_noise(mot)))
    print(remove_noise(mot))