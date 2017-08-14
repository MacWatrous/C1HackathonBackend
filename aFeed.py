import json
from TwitterDay import TwitterClient
import TwitterDay
import psycopg2
from time import gmtime, strftime


class AFeed(object):
    result = []
    def __init__(self):
        dayFetcher = TwitterDay
        self.result = dayFetcher.main(1)
        #do stuff here to get the days sentiment
        #end of day store days sentiment

    def getSentiment(self):
        return json.dumps(self.result)
