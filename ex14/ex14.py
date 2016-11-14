# Lesson 14 -- Now that the file is getting large, we need to reorganize it.

# In a large web application, there could be many forms and even more
# views. Putting them all into a single file becomes unmanageable,
# especially if multiple people are working on it. We are going to
# refactor both the python files and the html files to make it easier
# to manage.
#
# To Do:
# 1. Create a directory called animal_app. Move the templates
#    subirectory into it. Also add a static subdirectory and move any
#    images into it.
#
# 2. Create a file in animal_app and call it __init__.py. (When a
#    directory has a file with that name, Python treats the directory
#    as a Python package with the same name as the directory.) The new
#    file should contain just the following lines (without triple
#    quotes):
'''
from flask import Flask
import random, redis

Red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = hex(random.randrange(1<<128))  # 128 bits of randomness

import animal_app.views
'''
#
# 2. Create a file called forms.py inside animal_app and move all of
#    the forms from this file into that file. It will need to import
#    FlaskForm, the validators, and the field types.
# 
# 3. Create another file in animal_app and call it views.py. Now move
#    all of the views into that file. It will also need some imports,
#    which can then be removed from this file (unless it still uses
#    it). Be sure to import the forms, perhaps with
#        from forms import *
#    In addition, it will need app and Red from __init__.py. To
#    import those, you do not import __init__. Instead, use
#        from animal_app import app, Red
#    This creates a circular import where views imports __init__ and
#    __init__ import views. This is usually a bad idea, but it is the
#    common practice for Flask applications.
#
# 4. The only import left in this file should be import os. This file
#    will be the one you run when you want to run the server. So it
#    needs to import app from animal_app and then do the app.run command.
#    That should be it: two imports (app & os) and a run command.
#
# 5. That was a lot! Now it's time to test it. You may find that you
#    left some imports out or put them in the wrong file. These will
#    tend to give errors of the form:
#        NameError: global name '<something>' is not defined
#    In that case, find where it is needed and make sure to import the
#    right thing. If you get stuck on this, you can go ahead and use
#    the code from the next lesson.
#
# 6. We were not very careful with how we used the templates to make
#    our pages. At this point, if we wanted to change something so it
#    goes on every page, we would not be able to without changing
#    almost every file. So now we'll fix it. Take the parts in
#    base.html that are not appropriate for every page and move them
#    into animal.html. Then make request.html, login.html, and
#    management.html extend base.html. Test this to make sure it
#    works. To feel the benefit of this, now add something to the
#    base.html and see that it shows up on every page.

import os, json, redis, random, hashlib
from flask import redirect, url_for
from flask import Flask, render_template, session 
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange, Length
from wtforms import StringField, IntegerField, SelectMultipleField, \
     RadioField, TextAreaField, PasswordField, SubmitField


class RequestForm(FlaskForm):
    name  = StringField('Requested animal', [InputRequired()])

    scale = IntegerField('Awesomeness on a scale of 1-10',
        [NumberRange(min=1, max=10)] )

    power = SelectMultipleField("Animal's special power", choices = [
        ("speed", "Speed"), ("str", "Strength"), ("regen", "Regeneration"),
        ("invis", "Invisibility"), ("other", "Something Else") ])

    first = RadioField('Is this your first request?',
        [InputRequired(message="Law of Excluded Middle Violated")],
        choices = [ ('yes', 'Yes'), ('no', 'No') ])

    reason = TextAreaField('Why is this animal interesting? (100 characters max)',
        [Length(min=0,max=100)])

    submit = SubmitField()


Red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = hex(random.randrange(1<<128))  # 128 bits of randomness


class LoginForm(FlaskForm):
    '''A very basic login form'''
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField()

    
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'let-me-in':
            session["username"] = form.username.data
            session["favorite color"] = "Yellow"
            print "Admin logged in!"

            return redirect(url_for('hello'))  

        else:
            print "Invalid credentials: username '{}' and password '{}'".format(
                form.username.data, form.password.data)
        
    elif form.submit.data:
        print "Username or password not supplied"
            
    return render_template('login.html', form=form)


@app.route('/')
def hello():
    if session.get("username"):
        print "Favorite color", session["favorite color"]
        return 'Hello {}!\n{}'.format(session.get("username"), __file__)
    
    else:
        return 'Hello World!\n{}'.format(__file__)


@app.route('/animal/<animal_name>')
def animal(animal_name):
    data_as_json = Red.get('animal:' + animal_name)

    if data_as_json is not None:
        data = json.loads(data_as_json)
        count = Red.incr('count')
        return render_template('animal.html', num_views=count, **data)
    else:
        return "Oops, I don't know about {}".format(animal_name)

    
@app.route('/request', methods=['post', 'get'])
def animal_req():
    form = RequestForm()
    if form.validate_on_submit():
        # Store request & update statistics on Redis
        req_id = Red.incr('num_requests')
        req_dict = form.data
        Red.set("request:{}".format(req_id), json.dumps(req_dict))
        get_back = json.loads(Red.get("request:{}".format(req_id)))
        req_animal_cnt = Red.incr('animal-request:{}'.format(req_dict['name']))
        # Debug information to terminal
        print "Animal '{}' has been requested {} times, including this time.".format(
            req_dict['name'], req_animal_cnt)

    else:
        if not form.submit.data:
            print 'No data was submitted'
        else:
            print 'Data was invalid'
            print 'Errors: {}'.format(form.errors)
                
    return render_template('request.html',form=form)


@app.route('/manage')
def manage():
    if "username" not in session:
        return redirect(url_for('login'))

    # Now let's grab the relevant Redis information (shortened)
    num_req = Red.get('num_requests')
    num_req_dict = { key[key.find(':')+1:] : Red.get(key)
                     for key in Red.scan_iter(match="animal-request:*") }
    # We add the data from the requests
    req_detail = [ json.loads(Red.get(key))
                   for key in Red.scan_iter(match="request:*") ]
    # Also, management.html has been updated accordingly
    return render_template('management.html', total=num_req,
                               by_animal=num_req_dict,
                               details=req_detail)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# -- See above. The to do items are listed at the top in this lesson.
