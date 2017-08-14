import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import sys


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        return analysis.sentiment.polarity
        """
        if analysis.sentiment.polarity > 0:
            if analysis.sentiment.polarity > 0.8:
                print(tweet)
                print(analysis.sentiment.polarity)
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            print(tweet)
            print(analysis.sentiment.polarity)
            return 'negative'
        """
    def get_tweets(self, query, since, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        counter = 0

        try:
            # call twitter api to fetch tweet and set up dictionary
            fetched_tweets = self.api.search(q=query, since=since, count=1)
            # call to twitter api to fetch remaining tweets matching the query
            for tweet in tweepy.Cursor(self.api.search, q=query, since=since, count=count).items(count):
                fetched_tweets.append(tweet)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                parsed_tweet = {}
                # Further ensure tweet is for capital one
                if "capital one" in (tweet.text).lower() or "capitalone" in (tweet.text).lower() or "@CapitalOne" in (
                tweet.text):
                    parsed_tweet['text'] = tweet.text
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                    parsed_tweet['id'] = tweet.id
                    #print(tweet.id)
                    #print "\n\n"
                    #print(tweet)
                    #print "\n\n"
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
                #print(tweet.created_at)
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(argv):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets from x date
    if argv == 1:
        #just grab tweet ids, grab 5ish
        tweets = api.get_tweets(query='\"capitalone\" OR \"capital one\"', since="2017-06-08", count=30)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] > 0]
        ids = []
        for tweet in ptweets[:5]:
            ids.append(tweet['id'])
        #print ids
        return ids


    else:
        #grab whole day
        tweets = api.get_tweets(query='\"capitalone\" OR \"capital one\"', since="2017-06-08", count=5000)

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] > 0]
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] < 0]
        neuttweets = len(tweets) - len(ntweets) - len(ptweets)

        #print("\nPositive tweets: {}".format(len(ptweets)))
        #print("Negative tweets: {}".format(len(ntweets)))
        #print("Total tweets: {}".format(len(tweets)))
        return [len(ptweets), len(ntweets), neuttweets, len(tweets)]



if __name__ == "__main__":
    # calling main function
    main(sys.argv[1:])