# Ex8 -- We clean things up by offloading the data to a json file

import os
import json                        # NEW: We'll need this to load the data
from flask import Flask
from flask import render_template  

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)

# We have now removed all of the animal_data and put it into a file
# called animal_data.json. JSON is a web standard that makes it easy
# to work with dictionaries, lists, strings, and numbers. It looks a
# lot like Python, but with a couple of main differences:
#    1. Strings require double-quotes (Python uses single & double quotes)
#    2. In addition to dictionaries and lists, only strings, booleans,
#       and numbers are allowed. You cannot store other information,
#       such as a file handle or a function, unless you can convert it
#       to and from acceptable types.
#    3. JSON makes no distinction between numbers; they are all treated as
#       double-precision floating point numbers. This means when you load
#       JSON data you may need to convert the numbers back into integers.
#    4. All strings are treated as Unicode.


# Since animal data is now in a file, we need to load it. Loading JSON
# data turns out to be very easy. Note that it's two nested functions:
# open is used to access the file and json.load is used to convert it to
# a python value.

animal_data = json.load(open('animal_data.json'))

# Since animal_data is a Python dict, you can add keys using the update
# method. In the next line, we load another json object for a dictionary
# from a file and add its keys to the animal_data dictionary.

animal_data.update( json.load(open('more_animal_data.json')) )


@app.route('/animal/<animal_name>')
def animal(animal_name):
    if animal_name in animal_data:
        return render_template('animal.html', **animal_data[animal_name])
    else:
        return "Oops, I don't know about {}".format(animal_name)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. Check to see that you can view the url for the animal in the
#    more_animal_data.json file.
# 2. Add "cephalopod" key to more_animal_data.json and just give it a
#    title. To view it, even in debug mode, you'll
#    need to restart the server because changing data files doesn't
#    trigger a restart. (Tip: rather than using Ctrl-C in the terminal
#    and rerunning the server, you can just make a trivial change in
#    the file, like adding and removing a space, and then re-save it.)
#    What happens when you try to view it? Can you fix it?
# 3. Suppose we want to keep track of how many times a web page is
#    viewed using some persistent data. (Persistent means the data is
#    not erased even if the server shuts down and starts over.) We can
#    do this using a JSON file. Create a new JSON file called
#    count.json that just has the number 0 in it and nothing else
#    (i.e., no curly braces, no brackets, no commas).
# 4. Add a line loads count.json into a variable called count inside
#    the animal view. (Hint: It should look a lot like the line that loads
#    animal_data.json.) Where should it go? Then increase the count
#    variable by one, since the number of views is going up by one.
# 5. Now we need to display this new number, so we need to update
#    (a) the information sent to the template and (b) how the template
#    handles the information.
#    (a) Before **animal_data[animal_name], add an argument that looks
#        like "num_views=count" but without the quotes.  Note that
#        when you use ** in an argument list it must come last.
#    (b) Open up templates/base.html. The template will get the new
#        information as a variable called num_views because that's
#        what we called it. Put it somewhere on the page by using the
#        variable {{ num_views }}, preferably in a
#        sentence. (Alternatively, you could put it in animal.html.)
#    Test this in your browser. Notice that repeated views do not
#    increase the count.
# 6. Lastly, we need to update the file count.json so that the count
#    goes up by one every time we reload it. Go back into the animal
#    view and add the following line to save the number as a json
#    object.
#        json.dump(count, open('count.json','w'))
#    Where should this line go? Now every time you reload a page, the
#    count should keep go up by one.
# 7. Make sure it really is a persistent store by stopping and
#    re-starting the server. Did it remember the number of page views?
#    Look at count.json and verify that it's changed.
# 8. Change the JSON file to a different number and view it again.
#    You can make it show 1000 or 1000000 if you want. Notice, too
#    that there is no "type checking" of the number, so long as it is
#    a number. This means you can set the number of views to a fraction
#    or a negative number. Try it.

# Using json files can be a good choice if you have a lot of data and
# you will almost never change it. However, if there are a lot of
# parts that are changing, reading and writing to file for each one
# can be slow. Also, using a file doesn't let you use all the
# advantages of databases, like using advanced searches, automatic
# keys, type checking, relationships between data, and so on.

# For our purposes, the worse thing about using a JSON file is that it
# scales poorly. If a thousand people visit your site in the same
# second, the hard drive will probably not keep up. This could lead to
# significant lag loading your page. Also, you can get a race
# condition, which is where the timing of different events effect the
# outcome. In this case you could have two different instances read
# the number, each add one, and then save the updated number. In this
# case, only one visit would be counted.

# All of these issues are addressed by using a data store that scales
# well to multiple users. Two of the most commly used technologies for
# this are MySQL and PostgreSQL. These are relational SQL databases
# that allow you to make advanced queries. They are a good option in
# many cases, but the learning curve can be pretty steep.

# Our approach in this tutorial will be to use a NoSQL data
# store. While it will lack the advanced search capabilities of an SQL
# database, it is probably the quickest way to get up and running with
# a scalable data store that will prevent race conditions and lag.
