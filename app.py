import os
import numpy as np
import pandas as pd
import quandl
import datetime
from flask import Flask, render_template, request, redirect

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

   # Get today's date and set past month date:
   now = datetime.datetime.now()
   today = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
   pastmonth = now.month - 1
   year = now.year
   if pastmonth == 0:
      pastmonth = 12
      year = now.year - 1
   pastday = now.day if now.day < 29 else 28
   lastmonth = str(year) + '-' + str(pastmonth) + '-' + str(pastday)

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
      data = quandl.Dataset(dataset).data(params={'start_date':lastmonth,
                                                  'end_date':today
                                                 })
      df = data.to_pandas()
      print df
      return " Congrats!"


if __name__ == '__main__':
   app.run(port=33507)

