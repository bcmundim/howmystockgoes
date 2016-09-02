import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
   return redirect('/index')

@app.route('/index')
def index():
   try:
      API_KEY = os.environ['QUANDL_API_KEY']
   except KeyError:
      print "Not possible to load the environment variable 'QUANDL_API_KEY'"
      print 'Set API_KEY="" '
      API_KEY = ""
  
   return render_template('index.html')

if __name__ == '__main__':
   app.run(port=33507)
