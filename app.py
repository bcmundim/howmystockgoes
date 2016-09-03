import os
import numpy as np
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

      if np.any(select):
         return " Congratulations! You selected at least one property!"
      else:
         return " Please select at least one desired feature!"


if __name__ == '__main__':
   app.run(port=33507)

