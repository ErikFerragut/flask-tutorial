# Ex10 -- We update the webserver to use Redis

import os
import json
from flask import Flask
from flask import render_template  
import redis                      # New: Import redis module

Red = redis.StrictRedis()         # New: Create the Redis connection

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)

# Here, we used to load the data from a file, like this
#      animal_data = json.load(open('animal_data.json'))
# but this is no longer needed.

@app.route('/animal/<animal_name>')
def animal(animal_name):
    # First, we try to get the data from Redis
    data_as_json = Red.get(animal_name)

    # It was in there if data_as_json is not None
    if data_as_json is not None:
        # In this case, we just need to turn it back into a dictionary
        data = json.loads(data_as_json)
        # And then we send it to render_template, taking the place of
        # animal_data[animal_name] from ex08.
        return render_template('animal.html', **data)
    else:
        # This is the case if Redis returned None
        return "Oops, I don't know about {}".format(animal_name)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# Before doing the items below, make sure the Redis server is running.

# To Do:
# 1. Run ex10.py and see that the migration to Redis succeeded.
#
# We will now recreate the counter functionality from exercise 8.
# This will use the Redis incr command that takes a value, increments
# it, stores the incremented value, and returns it.  (Incrementing a
# value means adding 1.)
#
# 2. (a) Go back into base.html and have it use a value called num_views
#    using the expression '{{ num_views }}' somewhere.
#    (b) Right after the "data =" line in the animal function, add the
#    following line to grab, increment, store, and return the counter
#    (all in one step).
#          count = Red.incr('count')
#    This will work even without initializing the count key in Redis.
#    (c) Also, pass the count variable to the tamplate as "num_views=count"
#    and again be sure to put it before "**data"
#    Now test it.
# 3. After running the count up a bit, you can get at it from the
#    redis command-line interface (CLI) by running redis-cli
#    and then typing "GET count". Try it.
#
# One advantage of keeping the data in a JSON file was that it was
# easy to modify using a text editor. Now that the data is in Redis,
# we need a new approach. We'll look at three ways to do it. In each
# case, the updates to Redis will show up in the web server without
# requiring a server restart. This is an improvement over our older
# versions.
#
# 4. The simplest method is to just go back to exercise 9 and
#    modify the file animal_data.json. Then rerun the last few lines of
#    ex09.py to push those changes to Redis. Try this and make sure it
#    works.
# 5. Make the updates using redis-cli. Run it and type "SET count 120"
#    and see that it works as expected. This method works well for
#    individual numbers and simple strings, but is much more difficult
#    to do correctly for complicated strings like our animal values.
#
# One last thing as a word of warning...
#
# We have a subtle mistake in our set up. What if we wanted to add
# Count Dracula to our animal database and used "count" as the key?
# This would conflict with using "count" to count web views. What we
# should have done was use keys that disambiguate these cases.  For
# example, the animals keys could be "animal:cephelapod",
# "animal:slug", and "animal:vulture". There would then be no way to
# conflict with "count". We should probably also be more specific and
# use "number of web views" rather than "count" to make it more
# informative and less likely to conflict in the future.
#
# 6. Fix the variable naming error in your redis server by running
#    the following python code (without the triple quotes)
'''
import json
import redis

Red = redis.StrictRedis()
for key in ['cephalopod', 'vulture', 'slug']:
    Red.set('animal:' + key, Red.get(key))
    Red.delete(key)    # optional: get rid of the old keys
'''
# 7. After this, the code above will no longer work. Fix the Red.get
#    command so it works again.

