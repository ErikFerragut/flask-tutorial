# Ex11 -- We use a first form and show the results in a view
# Ex12 -- Forms with validators
# Ex13 -- Now do something fun with it

# First of all, we need to install flask-wtf, a flask extension for
# handling forms. In Cloud9 it should already be installed. Otherwise,
# use
#     pip install Flask-WTF
# If that throws an error, you might try
#     sudo pip install flast-wtf
#
# If all is well, it will also install WTForms, if not you'll need to
# install that separately.

import os
import json
from flask import Flask
from flask import render_template  
import redis
import wtforms                    # NEW: underlying forms module
import flask_wtf                  # NEW: module to help with forms in Flask

# To use forms, we will (1) create a python class for each form we
# want to use, (2) provide views to respond to the results, and (3)
# create templates for both the form and the response to the form.

# We begin by creating the class, which we must inherit form
# FlaskForm.  This will be a form where people can request new animals
# they'd like to see web pages developed for.
class RequestForm(flask_wtf.FlaskForm):
    # We put all of the fields inside as class variable rather than
    # putting them in the __init__ method. Each is given by a type and
    # a name. wtforms has 15 field types built in. Here we show just
    # the few most commonly used.

    # The general pattern is
    #   variable = wtforms.<FieldType>(how it shows up in the form)

    # StringField and IntegerField view the input as a string and integer, resp.
    name  = wtforms.StringField('Requested animal')
    scale = wtforms.IntegerField('Awesomeness on a scale of 1-10')

    # SelectField is a drop-down menu of a fixed list of options.
    # Here we list the 35 animal phyla.
    power = wtforms.SelectField("Animal's special power", choices = [
        ("speed", "Speed"), ("str", "Strength"), ("regen", "Regeneration"),
        ("invis", "Invisibility"), ("none", "None"), ("other", "Something Else") ])

    # Radio buttons are not used as much as they used to be. They
    # are a set of mutually exclusive options (like SelectField options)
    # but where all options are presented at once, and one must be chosen
    # by clicking on the button next to it.
    first = wtforms.RadioField('Is this your first request?',
        choices = [ ('yes', 'Yes'), ('no', 'No') ])

    # The TextAreaField type is a box in which they can write something.
    reason = wtforms.TextAreaField('Why is this animal interesting?')

    # Forms typically have a button that indicates the user is done
    # filling it out. Pressing the button makes the browser submit the
    # data to the server.
    submit = wtforms.SubmitField()
    
    # See http://wtforms.simplecodes.com/docs/0.6.1/fields.html#basic-fields
    # for the full list


Red = redis.StrictRedis()
app = Flask(__name__)

# To prevent a security weakness in Forms, we add a secret key to the
# app.  Make it hard to guess.
app.secret_key = 'dontguessme584829038572'

# This part's the same...
@app.route('/')
def hello():
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

# A new view provide the form and handle the submission.  Note the
# methods argument provides a list of the strings post and get. In web
# traffic (i.e., HTTP), there are five actions: POST, GET, PUT, PATCH,
# and DELETE. POST is used to create new data. GET is used to read
# data. PUT is used to update or replace data. PATCH and DELETE are
# less commonly used. Here, this same function is used for both POST
# and GET. In other views where no method is specified, it is just for
# GET by default.
@app.route('/request', methods=['post', 'get'])
def animal_req():
    # We instantiate a RequestForm object
    form = RequestForm()
    # validate_on_submit is True if a form was posted and it
    # validates. We will discuss validation more in the next exercise.
    # Even though the form information was not passed into the
    # function, it is made available to form by the route
    # decorator. This prevents having to pass in context variables to
    # every view.
    if form.validate_on_submit():
        # We print the received data. This will show up in the
        # terminal where you are running this server.
        print 'Data was valid'
        print "Name: '{}'".format(form.name.data)
        print "Scale: '{}'".format(form.scale.data)
        print "Power: '{}'".format(form.power.data)
        print "First: '{}'".format(form.first.data)
        print "Reason: '{}'".format(form.reason.data)
        print "Submit: '{}'".format(form.submit.data)
    else:
        # Data was either not received or not
        # validated. form.submit.data is a boolean that will be True
        # if a form was submitted.
        if not form.submit.data:
            print 'No data was submitted'
        else:
            print 'Data was invalid'
            print 'Errors: {}'.format(form.errors)
    return render_template('request.html',form=form)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. Look at templates/request.html. Notice how none of the labels or
#    html input types are hard coded into the page. The use of the
#    <div> tag puts each field on a new line. We'll learn more about
#    that when we get to html formatting. Also note the
#    form.hidden_tag() function. This is where the secret_key is used
#    to prevent hijacking of forms. Go to the /request view and
#    compare the result to the file request.html. See how, except for
#    hidden_tag, each piece shows up in the browser. What is the label
#    and what does the function call do?
# 2. Look at the server output in the terminal. What does it say? Where in the 
#    Python script was this printed? Does it make sense?
# 3. Now fill out the form and click the submit button. You should see
#    new ouput in the server's terminal window. Was the form valid?
#    If so see if you can make sense of the data values. Submit
#    multiple times trying to get both valid and invalid results. See
#    what kind of errors you can get. (Hint: only the scale and first
#    can be invalidated from within a browser.)
# 4. You should now be able to tinker with the form. Try the following:
#    a. Change the labels on some of the fields in the class
#       definition and see the site change. The labels are the first
#       argument in each field definition.
#    b. Add options to the select and radio button fields within the
#       class and see that they become available in the browser.
#    c. Allowing only one super power for an animal is kind of
#       limited. Change SelectField to SelectMultipleField in the
#       class definition and test it out. What data does the server
#       report? Of course, now having None as an option makes no
#       sense, so you should remove that option.
# 5. Now we'll do some advanced testing. Using a browser is not the
#    only way to reach a web page. In fact, it's possible to
#    custom-make the form values. We'll use Firefox to customize a
#    form response. (It is also possible with other browsers.)
#    a. Click on tools and turn on developer tools on the request page
#    b. Click on the network tab in developer tools
#    c. Reload the page by hitting enter in the URL window. A single
#       row should appear that begins with a green dot, 200, and POST.
#       Click on that row.
#    d. A box should appear on the right. In that box, there's a button
#       that says Edit and Resend. Click that button. This will allow
#       you to forge a new form submission.
#    e. The last text area is called Request Body. This is what the
#       browser sends when it communicates with the server. The
#       general format is settings variable=value joined by '&'.
#       Go into that line, change things, and then resubmit. See
#       how the server reacts by looking at what is printed in the
#       server's terminal window.

