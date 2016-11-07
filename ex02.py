# Ex2 -- We learn how to use routes

import os   
from flask import Flask

app = Flask(__name__)     # create an app

# This is just like before
@app.route('/')           
def hello():              
  # we add the filename so we can tell future servers apart more easily
  return 'Hello World!\n{}'.format(__file__)

# Now we add some more routes. Each route/function pair is called a "view"
@app.route('/wildcats')
def wildcats():
  return 'Go Team!'
    
@app.route('/really/long/url')
def longone():                # note the function name needn't match the route
    return (r'''<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Favorite Food</th>
  </tr>
  <tr>
    <td>Leonardo</td>
    <td>da Vinci</td> 
    <td>Pop Tarts</td>
  </tr>
  <tr>
    <td>Genghis</td>
    <td>Khan</td> 
    <td>Hot Dogs</td>
  </tr>
</table>''')

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# Now run this with
#    python ex2.py
# from the command line

# To Do:
# 1. Figure out (by trial and error) which URLs take you to each route above
# 2. Add another route and function and make sure you can get to it
# 3. You can have multiple routes before a function, in which case any of them 
#    will work. Add an orhs route before the wildcats function and test it.
#    (If you get an error, read it carefully; it tells you how to fix it.)
# 4. Advanced: What happens if a route ends with a slash ('/')? The behavior
#    seems to depend on whether it's in a cloud9 browser pane or a separate tab.

