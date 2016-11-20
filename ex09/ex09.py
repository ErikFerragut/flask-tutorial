# In this example, we will begin using a Redis data store. If you are
# running in the tutorial workspace on Cloud9, you should already have
# Redis available. Jump ahead to the test, below.

# If you are not running on Cloud9 and Redis is not already installed,
# you need to install it. See the Redis documentation for how to do
# this on your platform. Briefly, you can use sudo apt-get install or
# brew install if you are on Ubuntu or Mac OS X (and are using
# Homebrew.) On Windows, it's a lot trickier. There's no official
# support, but an unoffical port to Windows at
# https://github.com/MSOpenTech/redis. If you are serious about making
# a web server and only have Windows, you are probably better off
# either using Cloud9 or running a virtual machine of Ubuntu.

# If you need to install the Python bindings for redis,
# simply run
#      sudo pip install redis

# This tutorial will be a bit different 

# In one terminal tab, run
#      redis-server
# to start the server.

# In another, run
#      redis-cli ping
# to see if the server is working. It should respond with
#      PONG

# If you are running on your own server, make sure that port 6379,
# 16379, and 26379 are blocked by your firewall since we will only
# be using it locally, which means we only connect to Redis from
# the same machine that is running it. Not only is this easier to
# secure, it reduces latency by avoiding network communication.

# Unlike the other labs, we first need to store the data in
# animal_data.json into the Redis server. First, we will run some
# basic examples to get used to it. You should type the following into
# a python session. (Pro Tip: Use ipython instead of python for
# interactive sessions.)

import json    # this will be for parsing json strings
import redis   # this is for connecting to redis

# Set up a connection to the Redis server
Red = redis.StrictRedis()

# An easy way to save values is with set(key, value)
result1 = Red.set("first-key", "a value associated with that key")
result2 = Red.set("second-key", "a value associated with the second key")

# The returned result is True if it worked
print "Result1: '{}'".format(result1)
print "Result2: '{}'".format(result2)

# An easy way to get values from keys is with get(key)
v1 = Red.get("first-key")
v2 = Red.get("second-key")
v3 = Red.get("third-key")

# It retrieves what you stored
print "v1: '{}'".format(v1)
print "v2: '{}'".format(v2)
print "v3: '{}'".format(v3)  # --> Or None if it hasn't been stored

# If you want to delete something, you can't just send it None
# because it will be viewed as a string
Red.set('first-key', None)
v = Red.get('first-key')
print v, type(v)            # --> v is not None, it's a string 'None'

# to delete a value, you use the delete command
n = Red.delete('first-key')
print n                     # --> result is 1, the # of things deleted (?)

# now we'll store some more complicated structures in Redis using JSON
complicated_structure = { 'key1': {'key1.1': 'value1.1',
                                   'key1.2': ['isnt', 'this', 'great?']},
                          'key2': {'2':'store data',
                                   '4':'ever'} }

# convert it to a JSON string (note the s after dump returns a string)
as_json = json.dumps(complicated_structure)
Red.set('complex structure as json', as_json)

# then later, we read it back
value = Red.get('complex structure as json')

# is it the same?
print value == complicated_structure
# --> False...  Not the same! value is a string, not the complicated structure.
print value == as_json
# --> True

# To get the complicated structure back, we use json.loads
structure2 = json.loads(value)
print structure2 == complicated_structure
# --> True...  It worked!

# This reconstruction doesn't always work. You'll see that below in the
# to do items.

# At this point, with set, get, and delete, you know enough to do
# persistent storage on Redis from Python.

# To Do:

# 1. Redis is persistent, but we haven't tested that yet. To see that
#    it is persistent, shut down the server (Ctrl-C in the terminal)
#    and start it back up (redis-server). If you try to get values now
#    are they still there. Try "Red.get('second-key')", for example.
# 2. Change the keys in complicated_structure from the strings '2' and
#    '4' to just the numbers 2 and 4. Now what happens if you convert
#    it to JSON, save it to Redis, and then reload it?
# 3. There is only one Redis server running on your machine at a time.
#    This means that it can be used as a way to communicate between
#    different processes (although better methods exist). Run ipython
#    in two different terminal tabs. Import redis into each and create
#    a redis connection using Red = redis.StrictRedis(). Now set some
#    values in one terminal and get them in the other. This is how
#    different instances of Flask will be able to communicate.
# 4. Redis can do some other things, too. It can directly increment
#    counts using Red.incr(key). It can also append a string to the
#    end of a value using Red.append(key, thing_to_append). Try these
#    out.  If you're interested, more commands are documented at
#    http://redis.io/commands. Especially interesting are commands for
#    working with lists and sets. These start with L and S,
#    respectively.
# 5. What if the Redis server is down? Shutdown the server (using
#    Ctrl-C in the terminal) and then try a get or set command. What
#    happens? It's good to know what this looks like in case it
#    happens when you are testing your web server. It usually means
#    you forgot to start the server.
# 6. Run the code below to take the values in animal_data.json and
#    save it to your Redis data store. This will make it available
#    later when your web server needs it.

import json
import redis

# load the data from the json object
animal_data = json.load( open('animal_data.json') )

# get a new redis connection, just in case
Red = redis.StrictRedis()

# for each key in the animal_data dictionary, store the value as a
# json string inside of redis
for key, value in animal_data.iteritems():
    value_as_json = json.dumps(value)
    Red.set(key, value_as_json)


# you can test it:
print json.loads(Red.get('cephalopod'))

# (or in ipython terminal, the following pretty prints it)
json.loads(Red.get('cephalopod'))
               
