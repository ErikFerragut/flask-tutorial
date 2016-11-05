# Ex7 -- We use some in-template logic

import os   
from flask import Flask
from flask import render_template  

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)

# We now get rid of all animal pages, except for the data-generated ones
# Note, however, that the fact_lists used to look like this:
#      '''<ol>
#           <li>Slugs can be as long as 10 inches</li> 
#           <li>Slugs can flatten themselves to 1/20th their height</li>
#           <li>An acre of farmland contains 250,000 slugs</li>
#           <li>Slugs can live as long as 6 years</li>
#         </ol>'''
# and now are lists of strings. Also, the img_link has been turned into a
# dictionary with two fields.
animal_data = { 
  "slug": { 
      "title":"Slugs",
      "source_url":"http://www.softschools.com/facts/animals/slug_facts/1246/",
      "fact_list": [
          "Slugs can be as long as 10 inches",
          "Slugs can flatten themselves to 1/20th their height",
          "An acre of farmland contains 250,000 slugs",
          "Slugs can live as long as 6 years" ],
      "img_link": {"src":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Ambigolimax.jpg/330px-Ambigolimax.jpg",
          "alt":"A slug"}
    },
  "cephalopod": {
      "title":"Cephalopods",
      "source_url":"http://hubpages.com/education/Octopus-Squid-and-Cuttlefish-10-Weird-Fun-Facts-About-Cephalopods",
      "fact_list": [
           "Cephalopods have beaks and tongues", 
           "Cephalopods have poisonous spit",
           "Cephalopods are predators",
           "Cephalopods have the superhero trait of jet propulsion",
           "Cephalopods can break off their arms and regenerate new ones",
           "Cephalopods can grow as large as sixty feet and weigh more than half a ton"],
      "img_link": {"src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Octopus3.jpg/330px-Octopus3.jpg", 
         "alt":"Swimming octopus, from wikimedia commons" }
    }
}    
   
# To make this work, we had to change animal.html to use the lists and
# the fields. Since the number of items in the list can vary, the
# template needs to do its own loops. We also added an if statement in
# case no title is given. These changes are all in animal.html; the
# animal view (i.e., this function and decorator) remains the same.
@app.route('/animal/<animal_name>')
def animal(animal_name):
    if animal_name in animal_data:
        return render_template('animal.html', **animal_data[animal_name])
    else:
        return "Oops, I don't know about {}".format(animal_name)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. Read the new animal.html, comparing to the one from ex6 if
#    needed.  Notice the loop structure (for fact in fact_list) and
#    the field elements (img_link.src and img_link.alt). Look how the
#    if statement is used to determine whether to show the title
#    variable or a default. Comment out the title field for one of the
#    animals and see that the if statement does what you expect.
# 2. Add a new field to each animal in the animal_data dictionary. For
#    example, you could add another image, a motto, a favorite book,
#    or whatever else you can think of. Then update animal.html so
#    that the new field will show up in the rendered web page.
# 3. There are a lot more templating tricks that you can use. These
#    are pretty well described at
#    http://jinja.pocoo.org/docs/dev/templates/. Find something on
#    that page to try. (The if command may be a good one to start with
#    since there are so many ways to use it. Also, using loop
#    properties like loop.first and loop.last might be good.
# 4. Inheritances can chain. Create a new file called nofact.html that
#    extends animal.html to get rid of the fact list. Then create a
#    view for it of the form /nofact/<animal_name>. Does it render
#    pages as you would expect? What's the difference between getting
#    rid of the fact list and making it empty inside of nofact.html?

