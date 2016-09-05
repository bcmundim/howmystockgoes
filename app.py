import os
import numpy as np
import pandas as pd
import quandl
import datetime
from flask import Flask, render_template, request, redirect
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components 

app = Flask(__name__)

@app.route('/')
def main():
   return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
   try:
      API_KEY = os.environ['QUANDL_API_KEY']
   except KeyError:
      print "Not possible to load the environment variable 'QUANDL_API_KEY'"
      print 'Set API_KEY="" '
      API_KEY = ""

   # Get Quandl API from the environment and set api version:
   quandl.ApiConfig.api_key = API_KEY
   quandl.ApiConfig.api_version = '2015-04-09'

   # Get today's date and set past month date or past year:
   now = datetime.datetime.now()
   today = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
   pastmonth = now.month - 1
   year = now.year
   pastyear = year - 1
   if pastmonth == 0:
      pastmonth = 12
      year = now.year - 1
   pastday = now.day if now.day < 29 else 28
   frompastmonth = str(year) + '-' + str(pastmonth) + '-' + str(pastday)
   frompastyear = str(pastyear) + '-' + str(now.month) + '-' + str(now.day)


   # Initialize default criterias:
   select = [
   False, # closing price
   False, # adjusted closing price
   False, # opening price
   False  # adjusted opening price
   ]

   if request.method == 'GET':  
      return render_template('index.html')
   else:

      try:
         ticker = request.form['ticker']
         if ticker == '':
            return " Please choose a stock ticker first!"
      except KeyError:
         return " Please choose a stock ticker first!"

      try:
         select[0] = request.form['closing_price'] == 'yes'
      except KeyError:
         select[0] = False

      try:
         select[1] = request.form['adjusted_closing_price'] == 'yes'
      except KeyError:
         select[1] = False

      try:
         select[2] = request.form['opening_price'] == 'yes'
      except KeyError:
         select[2] = False

      try:
         select[3] = request.form['adjusted_opening_price'] == 'yes'
      except KeyError:
         select[3] = False

      if not np.any(select):
         return " Please select at least one desired feature!"

      database = 'WIKI'
      dataset = database + '/' + ticker
      data = quandl.Dataset(dataset).data(params={'start_date':frompastyear,
                                                  'end_date':today
                                                  #'collapse':'annual',
                                                  #'transformation':'rdiff',
                                                  #'rows':4 
                                                 })
      df = data.to_pandas()

      #print df.columns
      # Index([u'Open', u'High', u'Low', u'Close', u'Volume', u'Ex-Dividend',
      # u'Split Ratio', u'Adj. Open', u'Adj. High', u'Adj. Low', u'Adj. Close',
      # u'Adj. Volume'],
      # dtype='object')

      #print df.head()
      #print df['Open'], df['Close'], df['Adj. Open'], df['Adj. Close']

      # Make sure Bokeh knows the index is of Data Time kind:
      #plot = figure(tools=TOOLS,
      plot = figure(
              title='Data from Quandl WIKI set',
              x_axis_label='Date',
              y_axis_label='Price',
              x_axis_type='datetime')

      # NOTE: Instead of df.index.to_series() below, df.index also works fine.
      if select[0]: # closing price
         plot.line(df.index.to_series(),df['Close'],
                   legend = ticker + ':' + 'Close',
                   color = 'red')
      if select[1]: # adjusted closing price
         plot.line(df.index.to_series(),df['Adj. Close'],
                   legend = ticker + ':' + 'Adj. Close',
                   color = 'orange')
      if select[2]: # opening price
         plot.line(df.index.to_series(),df['Open'],
                   legend = ticker + ':' + 'Open',
                   color = 'green')
      if select[3]: # adjusted opening price
         plot.line(df.index.to_series(),df['Adj. Open'],
                   legend = ticker + ':' + 'Adj. Open',
                   color = 'blue')

      # Render Bokeh plot components:
      script, div = components(plot)
      return render_template('graph.html', 
                              script=script, 
                              div=div,
                              version=bokeh.__version__,
                              ticker=ticker
                            )


if __name__ == '__main__':
   app.run(port=33507)

