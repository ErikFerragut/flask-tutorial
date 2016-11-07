# Ex12 -- We validate forms using wtforms.validators
# Ex13 -- Now do something fun with it

import os
import json
from flask import Flask
from flask import render_template
import redis
import wtforms
import flask_wtf

# Here is the class without all of the comments, but now we've begun
# adding validators to the input fields. When the form input is
# validated at the server using validate_on_submit, each of these
# validations is checked.  If any of them fail, meaning that the input
# didn't have the right form, the form "does not validate" and errors
# are produced. Last time, we just printed these errors. (The errors were
# in form.errors.)
class RequestForm(flask_wtf.FlaskForm):
    # We can't really process a request if you don't name the animal,
    # so we'll make it reject the form if name is left blank. Notice
    # how the validators for the field are in a list. All of the built
    # in validators are in wtforms.validators.*. Also, you don't just
    # list the validators, you have to call it as a function.
    name  = wtforms.StringField('Requested animal', [wtforms.validators.InputRequired()])

    # Integer fields already check to see that the input is an
    # integer, but we saw last time that you can enter numbers less
    # than 0 or more than 10 without triggering an error. Let's bound
    # the range with NumberRange(min, max).
    scale = wtforms.IntegerField('Awesomeness on a scale of 1-10',
        [wtforms.validators.NumberRange(min=1, max=10)] )

    # We've changed it to a SelectMultipleField and removed None as
    # per the last exercise. ****
    power = wtforms.SelectMultipleField("Animal's special power", choices = [
        ("speed", "Speed"), ("str", "Strength"), ("regen", "Regeneration"),
        ("invis", "Invisibility"), ("other", "Something Else") ])

    # It is possible to not make a choice for a radio buttom in most
    # browsers since it starts without selecting a button and then
    # allows you to submit it with no button selected. (However, once
    # you select a button, you can't usually unselect it.) We want to
    # make sure an option is picked. Notice that the validators go
    # before the choices.
    first = wtforms.RadioField('Is this your first request?',
        [wtforms.validators.InputRequired()],
        choices = [ ('yes', 'Yes'), ('no', 'No') ])


    # We'll add a validator to this one in the to do list below.
    reason = wtforms.TextAreaField('Why is this animal interesting?')

    # No validation needed on the submit button.
    submit = wtforms.SubmitField()


Red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = 'dontguessme584829038572'

# This part's the same...
@app.route('/')
def hello():
    return 'Hello World!\n{}'.format(__file__)


@app.route('/animal/<animal_name>')
def animal(animal_name):
    data_as_json = Red.get(animal_name)

    if data_as_json is not None:
        data = json.loads(data_as_json)
        count = Red.incr('count')
        return render_template('animal.html', num_views=count, **data)
    else:
        return "Oops, I don't know about {}".format(animal_name)

# This is the same
@app.route('/request', methods=['post', 'get'])
def request():
    form = RequestForm()
    if form.validate_on_submit():
        print 'Data was valid'
        print "Name: '{}'".format(form.name.data)
        print "Scale: '{}'".format(form.scale.data)
        print "Power: '{}'".format(form.power.data)
        print "First: '{}'".format(form.first.data)
        print "Reason: '{}'".format(form.reason.data)
        print "Submit: '{}'".format(form.submit.data)
    else:
        if not form.submit.data:
            print 'No data was submitted'
        else:
            print 'Data was invalid'
            print 'Errors: {}'.format(form.errors)
                
    return render_template('request.html',form=form)


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:

# 1. Test the validators by trying to make each one get an error. This
#    will be easiest if you have the terminal and the browser
#    side-by-side so you can quickly see the error messages.
#
# 2. We want the reason given in the form to not be too long. Look at
#    the validator documentation at the function Length at
#    http://wtforms.readthedocs.io/en/latest/validators.html and use
#    it to limit the text area to 100 characters. To be kind to the
#    user, add a character limit to the display. This should be done
#    by modifying the form class, not by modifying the html.
#
# 3. Validators all also take an optional message field that replaces
#    how the error is described. It is generally the last
#    argument. Use message field in a InputRequired validator for the
#    radio button to change the error comment to "Law of Excluded
#    Middle Violated" and test it. (For more information on that, see
#    https://en.wikipedia.org/wiki/Law_of_excluded_middle .)
#
# We haven't done anything with the form data. So let's do some Redis
# storing and tabulating. This will happen after the data is printed
# and before the else in the request view.
#
# 4. First, let's give the request a unique ID, which we'll do by just
#    counting up by one. Add a line to increment a number of requests
#    counter inside of Redis and to store the number in a variable.
#    This will look something like the count that keeps track of web views.
#    Also print this number out to the terminal for debugging. Test it.
#
# 5. Now we'll store all of the data we just received into
#    Redis. First, turn the data received into a dictionary. The
#    dictionary fields should match the form fields: name, scale,
#    power, first, and reason. Then turn this dictionary into a json
#    object using json.dumps. Finally store it into redis using the
#    key "request:" followed by the request's unique ID from step 4.
#    Use redis-cli (with command GET request:1) to check that it
#    stored correctly.
#
# 6. Finally, we'll tabulate how many times each animal was requested.
#    Construct a key for the animal requested of the form
#    animal-request:<animal_name> and increment the count of that key.


