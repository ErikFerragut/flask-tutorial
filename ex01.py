# Ex1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "hello" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')           
def hello():              
    return 'Hello World!'

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# Run this in cloud9 by clicking on the green play button labeled Run.

# Also, make sure you can run this with 
#    python ex1.py
# from the command line

# To see the web page in another tab, go to the url, which is of the form
#   <workspace-name>-<user-name>.c9users.io:8080
# This is referred to as <url> below. 

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

# To Do:
#  1. Change the return statement in the function and see what happens
#  2. Change the @app.route('/') to @app.route('/<something-else>') and see what 
#     happens when you go to <url>:/ and <url>:/<something>

