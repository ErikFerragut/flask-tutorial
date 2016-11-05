# Ex6 -- We feed variables into templates

import os   
from flask import Flask
from flask import render_template  

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)

# Here is what the slug view using inheritance looked like
@app.route('/slug/')
def slug():
    return render_template('slug.html')

# The new thing in this exercise is that we can also feed variables into
# templates and have them inserted where we want. Look at animal.html. It 
# inherits from base.html and provides the title as "{{ title }}". This means
# that the value of the variable title will be put there. We can recreate
# the slug page as follows, where we put v2 in the title to distinguish it.
@app.route('/slug2/')
def ceph():
    return render_template('animal.html',
       title='Slugs v2',
       source_url='http://www.softschools.com/facts/animals/slug_facts/1246/',
       fact_list='''<ol>
  <li>Slugs can be as long as 10 inches</li> 
  <li>Slugs can flatten themselves to 1/20th their height</li>
  <li>An acre of farmland contains 250,000 slugs</li>
  <li>Slugs can live as long as 6 years</li>
</ol>''',
       img_link='''<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Ambigolimax.jpg/330px-Ambigolimax.jpg"
   alt="A slug"/>''')
   
# The slug and slug2 routes should look essentially the same. But aren't we 
# taking a step backward by introducing all this html back into our python?
# You bet. We'll fix it in two steps. First, we'll move it into a data structure
# and then we'll save that data in a data store (in a separate process from
# the server). We construct a dictionary of dictionaries to put all of our 
# data in.

animal_data = { 
  "slug": { 
      "title":"Slugs",
      "source_url":"http://www.softschools.com/facts/animals/slug_facts/1246/",
      "fact_list":'''<ol>
          <li>Slugs can be as long as 10 inches</li> 
          <li>Slugs can flatten themselves to 1/20th their height</li>
          <li>An acre of farmland contains 250,000 slugs</li>
          <li>Slugs can live as long as 6 years</li>
         </ol>''',
      "img_link":'''<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Ambigolimax.jpg/330px-Ambigolimax.jpg"
          alt="A slug"/>'''
    },
  "cephalopod": {
      "title":"Cephalopods",
      "source_url":"http://hubpages.com/education/Octopus-Squid-and-Cuttlefish-10-Weird-Fun-Facts-About-Cephalopods",
      "fact_list":'''<ol>
           <li>Cephalopods have beaks and tongues</li> 
           <li>Cephalopods have poisonous spit</li>
           <li>Cephalopods are predators</li>
           <li>Cephalopods have the superhero trait of jet propulsion</li>
           <li>Cephalopods can break off their arms and regenerate new ones</li>
           <li>Cephalopods can grow as large as sixty feet and weigh more than half a ton</li>
         </ol>''',
      "img_link":'''<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Octopus3.jpg/330px-Octopus3.jpg"
         alt="Swimming octopus, from wikimedia commons"/>'''
    }
}    
   
# And now we can construct a single view for both animals using a route variable
# and template variables together.
@app.route('/animal/<animal_name>')
def animal(animal_name):
    if animal_name in animal_data:  # check to make sure it's an animal we know
        # the ** means python should unpack the dictionary and use the keywords
        # as argument names and the values as the argument values.
        return render_template('animal.html', **animal_data[animal_name])
    else:
        return "Oops, I don't know about {}".format(animal_name)

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. In the animal.html file, it says "fact_list|safe" rather than just 
#    "fact_list". Why? Try removeing "|safe" and seeing what happens to slug.
# 2. Try going to /animal/cephalopod and /animal/slug. What happens if you go
#    to a different site, like /animal/carrot?
# 3. Take your animal example and add the relevant pieces to animal_data. Does
#    it render properly?
