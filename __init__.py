from flask import Flask
from aDay import ADay
from aMonth import AMonth
from aYear import AYear
from aRange import ARange
from aFeed import AFeed

app = Flask(__name__)


#2017-05-03
@app.route('/data/d')
def show_day_sentiment():
    aDayObj = ADay()
    return aDayObj.getSentiment()

#2017-05
@app.route('/data/m')
def show_month_sentiment():
    aMonthObj = AMonth()
    return aMonthObj.getSentiment()

#2017
@app.route('/data/y')
def show_year_sentiment():
    aYearObj = AYear()
    return aYearObj.getSentiment()

#2017-05-03,2017-06-01
@app.route('/data/r/<range>')
def show_range_sentiment(range):
    aRangeObj = ARange(range)
    return aRangeObj.getSentiment()

@app.route('/data/f')
def show_feed():
    aFeedObj = AFeed()
    return aFeedObj.getSentiment()

if __name__ == '__main__':
   app.run(debug = True)