import json
import psycopg2
from time import gmtime, strftime
from datetime import date, datetime
from flask.json import jsonify

class AYear(object):
    rows = []

    def __init__(self):

        mdy = strftime("%Y-%m-%d", gmtime())

        # SELECT * FROM main WHERE date >= '2017-05-02' ORDER BY date ASC LIMIT 30

        try:
            conn = psycopg2.connect(
                "dbname='d86041q8vqfr8h' user='cblxxgxfzcxhyc' host='ec2-23-21-220-48.compute-1.amazonaws.com' password='7dd5cfedce5ee3eba6ae1572007339c946cb0ae5b62b627351f41e425d2acc34' sslmode='require'")
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()

        try:
            cur.execute("""SELECT * FROM main WHERE date <= '""" + mdy + """"' ORDER BY date DESC LIMIT 365""")
        except:
            print("failed to store data")

        self.rows = cur.fetchall()

    def getSentiment(self):
        days = []
        arrReturnInner = []
        for row in self.rows:
            arrReturnInner.append({
                'time': row[0].isoformat(),
                'y': row[3]  # Neutral
            })
        days.append(arrReturnInner)
        arrReturnInner = []
        for row in self.rows:
            arrReturnInner.append({
                'time': row[0].isoformat(),
                'y': row[1],

            })
        days.append(arrReturnInner)
        arrReturnInner = []
        for row in self.rows:
            arrReturnInner.append({
                'time': row[0].isoformat(),
                'y': row[2],
            })
        days.append(arrReturnInner)

        # days.append({
        #     'date': row[0].isoformat(),
        #     'positiveNum': row[1],
        #     'negativeNum': row[2],
        #     'neutralNum': row[3],
        #     'totalNum': row[4]
        # })

        return json.dumps(days)