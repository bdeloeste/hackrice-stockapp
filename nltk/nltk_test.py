import nltk;
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import subjectivity

from nltk import tokenize


def getSentiments(sentences):
    from nltk import tokenize
    sid = SentimentIntensityAnalyzer()
    sentimtents = [None] * len(sentences)
    i = 0
    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        sentimtents[i] = ss['compound']
        i = i + 1
    return sentimtents


sen = [
    "Don't wanna RT a bunch of @realDonaldTrump... but Donald is carpet bombing @tedcruz right now and it's really entertaining.",
    "Greatly dishonest of @TedCruz to file a financial disclosure form & not list his lending banks- then pretend he is going to clean up Wall St"]
print(getSentiments(sen))
