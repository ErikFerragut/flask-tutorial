# Ex3 -- We learn how to put variables into our routes

import os   
from flask import Flask

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)


# Now, we put variables into the route with angle brackets.
@app.route('/resume/<skill>')
def resume(skill):               # the value is passed to the function
    return '''<p>Welcome to my resume page. 
    I am very good at knitting, programming, and {}.
    Please hire me.</p>'''.format(skill)

# You can also specify a type 
@app.route('/order/<int:orderid>')
def order(orderid):
    return '''Your order number {} will come up as soon as 
    we're done with order {}.'''.format(orderid, orderid-1)

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. Go to the site-url/resume/mathematics and see what happens. Choose other
#    URLs that will set the skill variable to other values. What happens if 
#    you use spaces in the URL?
# 2. Create a new view (i.e., route + function) that with route
#    @app.route('/<thing1>/<thing2>') and write a function taking arguments
#    thing1 and thing2.
# 3. See what URLs get the order function called and which don't. What about
#    following /order/ with "regular" integers, very big integers, negative
#    integers, fractions, or words? This sort of testing is often important to
#    find out if your web site will crash when used in a way you didn't expect.
