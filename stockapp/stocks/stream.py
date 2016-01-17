import sys
import json
import time

from datetime import datetime

import pusher as pusher
from pymongo import collection as col
from requests import packages
from settings import API, AUTH, MONGO, URL, STOP
from tweepy import StreamListener, streaming

from nltk.sentiment.vader import SentimentIntensityAnalyzer

p = pusher.Pusher(
        app_id='138191',
        key='b87e84a0194862d39bdd',
        secret='8fd41c3b939712649fbc',
)
p.trigger('test_channel', 'my_event', {'message': 'hello world'})

GOOGLE = ['google', '#google', 'android', 'chrome', 'docs', 'drive', 'translate', 'technology']
MICROSOFT = ['microsoft', '#microsoft', 'xbox', '#xbox', 'live', 'windows', 'office', 'word']
FACEBOOK = ['facebook', '#facebook', 'fb', '#fb']


class StreamFilter(object):
    """
    Object which handles the Twitter Stream filter parameters.
    """

    def __init__(self, stop_words, collection, max_tweets, geo_tweets=None):
        self.stop_words = stop_words
        self.collection = collection
        self.max_tweets = max_tweets
        self.geo_tweets = geo_tweets

    def get_stop_words(self):
        """
        :return: List[str]
        """
        return self.stop_words

    def get_collection(self):
        """
        :return: Pymongo Collection
        """
        return self.collection

    def get_max_tweets(self):
        """
        :return: int
        """
        return self.max_tweets


class CustomStreamListener(StreamListener):
    """
    Twitter Stream Listener
    """

    def __init__(self, api, stream_filter, filename=None, wtf=False):
        super(CustomStreamListener, self).__init__()
        self.api = api
        super(StreamListener, self).__init__()
        self.stream_filter = stream_filter
        self.key_list = []
        self.wtf = wtf
        self.logfile = 'logfile.log'
        self.google_price = 0
        self.microsoft_price = 0
        self.facebook_price = 0
        if filename is not None:
            self.filename = filename + '.txt'

    def on_data(self, data):
        data_dict = json.loads(data)
        try:
            if 'text' in data_dict:
                self.get_unique_tweets(data_dict)
        except KeyError, e:
            # TODO Log KeyError
            print >> sys.stderr, e
            self.log_error(str(e))

    def on_error(self, status_code):
        error_message = "Encountered error with status code: ", status_code
        print >> sys.stderr, error_message
        self.log_error(error_message)
        if status_code == 420:
            print "Sleeping for 15 min..."
            time.sleep(900)
        return True

    def on_timeout(self):
        error_message = "Timeout..."
        print >> sys.stderr, error_message
        self.log_error(error_message)
        return True

    def get_unique_tweets(self, data_dict):
        # TODO: Implement filter to check if Tweet text starts with 'RT'
        """
        :param data_dict:
        :return:
        """
        flag = False
        try:
            text = data_dict['text'].encode('ascii', 'ignore').lower()
            # Check for 'retweeted_status' in metadata field to determine
            # if tweet is a retweet (1st check)
            if 'retweeted_status' not in data_dict:
                url_match = URL.match(text)
                # Check if link contains url
                if url_match:
                    match_group = url_match.group()
                    if len(self.key_list) > 0:
                        if any(match_group in item for item in self.key_list):
                            flag = True
                        if flag is False:
                            data_dict['text'] = match_group
                            print "Inserted text: " + data_dict['text'] + '\n'
                            self.key_list.append(match_group)
                            sid = SentimentIntensityAnalyzer()
                            ss = sid.polarity_scores(text)
                            print ss['compound']
                            score = ss['compound']
                            for w in GOOGLE:
                                if w in text and self.google_price >= 0:
                                    self.google_price = score
                            for w in MICROSOFT:
                                if w in text and self.microsoft_price >= 0:
                                    self.microsoft_price = score
                            for w in FACEBOOK:
                                if w in text and self.facebook_price >= 0:
                                    self.facebook_price = score
                            p.trigger('test_channel', 'my_event',
                                      {'google': self.google_price,
                                       'microsoft': self.microsoft_price,
                                       'facebook': self.facebook_price})
                            self.google_price = 0
                            self.microsoft_price = 0
                            self.facebook_price = 0
                    else:
                        self.key_list.append(url_match.group())
        except TypeError, e:
            print >> sys.stderr, e
            self.log_error(str(e))
        return

    def get_geo_tweets(self, data_dict):
        """
        :param data_dict, List[coordinates]
        Filter and store stream data within a coordinate box
        :return
        """
        # TODO: Implement retrieving tweets within a coordinate box.
        try:
            if 'coordinates' in data_dict:
                if data_dict['coordinates'] is not None:
                    print "Collection size: " + \
                          str(self.stream_filter.collection.count())
                    print data_dict['coordinates']['coordinates']
                    self.stream_filter.collection.insert(data_dict)
                    with open('coordinates.txt', 'a') as outfile:
                        coordinates = data_dict['coordinates']['coordinates']
                        outfile.write(str(coordinates[0]) + ',' +
                                      str(coordinates[1]) + '\n')
        except KeyError, e:
            print >> sys.stderr, e
            self.log_error(str(e))
        return

    def log_error(self, error):
        """
        :param: Error string
        """
        with open(self.logfile, 'a') as outfile:
            outfile.write(error + str(datetime.now()) + '\n')
        return


def main():
    """
    Initialize Twitter stream parameters and start stream.
    :return: None
    """
    keywords = None
    stream_filter = None
    try:
        args = sys.argv[1:]
        if len(args) < 2:
            print >> sys.stderr, \
                "Usage: tweet.py [collection] [num of tweets] [keywords]" \
                "\n Leave [keywords] blank for mining geo-enabled Tweets."
            return
        collection = col.Collection(MONGO.test, sys.argv[1])
        max_tweets = sys.argv[2]
        stream_filter = StreamFilter(STOP, collection, max_tweets)
        if len(args) > 2:
            keywords = sys.argv[3:]

    except TypeError:
        print >> sys.stderr, "Caught TypeError"
    tweet_stream = streaming.Stream(AUTH,
                                    CustomStreamListener(API, stream_filter))
    while True:
        print "Starting new stream..."
        try:
            print "Getting unique Tweets:"
            tweet_stream.filter(languages=["en"], track=keywords)
        except packages.urllib3.exceptions.ProtocolError, e:
            print >> sys.stderr, e + "\nRestarting stream..."
            continue
        except packages.urllib3.exceptions.ReadTimeoutError, e:
            print >> sys.stderr, e + "\nRestarting stream..."
            continue
        except KeyboardInterrupt:
            tweet_stream.disconnect()
            break


if __name__ == '__main__':
    main()
