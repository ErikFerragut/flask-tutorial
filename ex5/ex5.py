# Ex5 -- We use templates for templating

import os   
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')           
def hello():              
    return 'Hello World!\n{}'.format(__file__)

# We now have two html files in the templates we can render: cephalopod & slug
@app.route('/ceph/')
def ceph():
    return render_template('cephalopod.html')

@app.route('/slug/')
def slug():
    return render_template('slug.html')

# These two new views look similar to the first two, but they use inheritance.
@app.route('/ceph2/')
def ceph2():
    return render_template('cephalopod2.html')

@app.route('/slug2/')
def slug2():
    return render_template('slug2.html')

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. First, go to the urls for cephalopod.html and slug.html and see what the
#    two have in common. Look at base.html and how it captures the common parts.
#    Notice how it uses {% block content %} to specify where stuff will go.
#    Now look at cephalopod2.html and slug2.html and see how they specify what
#    should go in each block.
# 2. I forgot to add that slugs have one lung. Add that in the right file at
#    the right place and see that it renders properly in the web site.
# 3. Seems I left the "This is the html file" line on every page. Remove it.
#    Wasn't that easier than changing in every single html file?
# 4. The blocks in slug.html simply overwrite the corresponding block in base,
#    but it doesn't need to fill in the block. Erase the title block in one of
#    the files to see how it renders differently (and compare to base.html).
# 5. Take your animal page that you created for exercise 4 and add it to this
#    server by creating a template that inherits from base.html and by adding
#    a view for it. Test it to make sure it works the way you expected.

