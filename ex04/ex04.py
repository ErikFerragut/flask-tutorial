# Ex4 -- We see why we need templates and how to use them

import os   
from flask import Flask
from flask import render_template  # NOTICE THIS: A new function we'll be using

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)


# So far, we've just produced simple pages, but what if we want to do something
# a bit more complicated?
@app.route('/ceph1/')
def ceph1(): 
    return '''<!DOCTYPE html>
<html>
<title>Facts about Animals</title>
<body>

<h1>Animals are amazing! Animals have superpowers! Read on!</h1>

<h1>Cephalopods</h1>
<p>Here are some
fun facts taken from 
<a href="http://hubpages.com/education/Octopus-Squid-and-Cuttlefish-10-Weird-Fun-Facts-About-Cephalopods">another site</a>.</p>
<ol>
  <li>Cephalopods have beaks and tongues</li> 
  <li>Cephalopods have poisonous spit</li>
  <li>Cephalopods are predators</li>
  <li>Cephalopods have the superhero trait of jet propulsion</li>
  <li>Cephalopods can break off their arms and regenerate new ones</li>
  <li>Cephalopods can grow as large as sixty feet and weigh more than half a ton</li>
</ol>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Octopus3.jpg/330px-Octopus3.jpg"
   alt="Swimming octopus, from wikimedia commons"/>
   
<h1>I mean, really? That's just wild!</h1>

<p>This is the quoted string.</p>
</body>
</html>'''

# This simple page is already getting out of hand (and we haven't even talked
# about CSS yet). Luckily, Flask provides templating as a tool for separating
# the logic from the content. Put another way, we get the HTML out of the Python.
# However, doing this requires using multiple files. In this case, we will use
# cephalopod.html. The following view should look identical to the ceph1 page
# except for the last paragraph that identifies which it is (quoted or html).
@app.route('/ceph2/')
def ceph2():
    return render_template('cephalopod.html')   # well, that was easy!



app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. Look at the cephalopod.html file in the templates sub-directory. It looks 
#    like the triple-quoted string above, but in a separate maintainable file.
# 2. Go to both URLs (routes) and compare how they render in the browser.
# 3. Pick another real or imaginary animal and create its html page modeled on
#    cephalopod.html. Make sure to put it in the templates sub-directory. Then
#    add a view for it and test it in the browser.
