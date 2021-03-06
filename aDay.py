import json
from TwitterDay import TwitterClient
import TwitterDay
import psycopg2
from time import gmtime, strftime


class ADay(object):
    result = []
    def __init__(self):
        dayFetcher = TwitterDay
        self.result = dayFetcher.main(0)
        #do stuff here to get the days sentiment
        #end of day store days sentiment

    def getSentiment(self):
        mdy = strftime("%Y-%m-%d", gmtime())

        arrReturn = []
        arrReturnInner = []
        arrReturnInner.append({
            'time': mdy,
            'y': self.result[2] #Neutral
        })
        arrReturn.append(arrReturnInner)
        arrReturnInner = []
        arrReturnInner.append({
            'time': mdy,
            'y': self.result[0],

        })
        arrReturn.append(arrReturnInner)
        arrReturnInner = []
        arrReturnInner.append({
            'time': mdy,
            'y': self.result[1],
        })
        arrReturn.append(arrReturnInner)
        #"""UPDATE main SET (positivenum, negativenum, neutralnum, totalnum) = ("""+self.result[0]+""", """ + self.result[1] + """, """ + self.result[2] + """, """ + self.result[3] + """) WHERE date IN(SELECT max(date) FROM myTable)"""

        try:
            conn = psycopg2.connect("dbname='' user='' host='' password='' sslmode='require'")
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()

        try:
            cur.execute("""UPDATE main SET (positivenum, negativenum, neutralnum, totalnum) = ("""+str(self.result[0])+""", """ + str(self.result[1]) + """, """ + str(self.result[2]) + """, """ + str(self.result[3]) + """) WHERE date IN(SELECT max(date) FROM main);""")
            conn.commit()
        except:
            print("failed to store data")

        return json.dumps(arrReturn)
