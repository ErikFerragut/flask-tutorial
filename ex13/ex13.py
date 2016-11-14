# Ex13 -- We introduce sessions

# In the previous lessons, we've shown how users can get around the
# web pages and use those pages to interact with a persistent data
# store. However, if the server supports more than one user (and it
# will!) we will need a way to track each individual user's
# information. A simple example is tracking each user's name so that
# we can reach back into Redis and grab their data. Or maybe the site
# involves multiple steps, like putting things in a cart, selecting a
# credit card, and then checking out. In that case, we need to keep
# track of these steps to make sure they all worked correctly, in the
# right order, and were done by the same user.
#
# A given user's interactions with a server are collectively called a
# "session".  Flask offers some methods for dealing with client-side
# sessions. You have probably heard of cookies. These are pieces of
# data that web servers put on your machine to make it easy for them
# to pick up where you left off. They are the main method for tracking
# sessions on the client (i.e., in the browser).
#
# A cookie is basically a key-value pair stored in the browser. Every
# time the user visits your site, they send all of your site-specific
# cookies with their request. It is possible to directly manage these
# using the request object, but we'll do it using the session object.
# It has the advantage of encrypting the data stored at the browser.


# We can put multiple imports per line to take less space
import os, json, redis, random                     # random is new
from flask import redirect, url_for   # these should have been taught earlier
from flask import Flask, render_template, session  # session is new
# Importing from allows us to use, e.g., FlaskForm instead of
# flask_wtf.FlaskForm
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
# Every time the secret key changes, the user cookies are no longer valid.
# So for testing purposes, it will be useful to have it change every time
# the server restarts. To do this, we use random.
app.secret_key = hex(random.randrange(1<<128))  # 128 bits of randomness


# The most common use for session is to manage authenticated
# users. That is, we want to let users tell us who they are and prove
# it with a password (or saved, encrypted cookie). Then we can give
# them access that's just for them. In this program, we're going to
# create a special administrator's login where administrators can see
# what has been requested. The first step will be to create a login
# view. It will have a form with username and password. First, we
# define the form.
class LoginForm(FlaskForm):
    username = StringField("Username", [InputRequired()])
    # using a password field uses the html form input type "password",
    # which tells the browser to not display the information as its
    # typed. Other than that, it's the same as a text or string input.
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField()

    
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Now we check to see if it is a valid login. Normally, this
        # would involve hashing the password and checking that against
        # the stored hash password for that username. This would be
        # easy to do with Redis. However, we'll just hard-code the
        # username and password.
        if form.username.data == 'admin' and form.password.data == 'let-me-in':
            print "Admin logged in!"
            # By route decorator magic, we have access to the session
            # variable, which allows us to store and retrieve
            # key-value pairs, much like a python dictionary
            session["username"] = form.username.data
            # We can also store other stuff if we want
            session["favorite color"] = "Yellow"
            
            # Go back to the index page (url_for takes function name as a string!)
            return redirect(url_for('hello'))  

        else:
            # This branch is followed if the form is valid, but the
            # credentials are not. We will put out a debug message for
            # the server. It is bad practice to be printing wrong
            # passwords, since even wrong passwords should be treated
            # as secrets. So don't do this in a real application.
            print "Invalid credentials: username '{}' and password '{}'".format(
                form.username.data, form.password.data)
        
    elif form.submit.data:
        # You only get here if the form validation failed. In this
        # case that means a required input was missing.
        print "Username or password not supplied"
            
    return render_template('login.html', form=form)


# Now we'll modify the index page to use the session information
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
        print 'Data was valid'
        print "Name: '{}'".format(form.name.data)
        print "Scale: '{}'".format(form.scale.data)
        print "Power: '{}'".format(form.power.data)
        print "First: '{}'".format(form.first.data)
        print "Reason: '{}'".format(form.reason.data)
        print "Submit: '{}'".format(form.submit.data)

        # The following was added from ex12
        # -- This is one more request, update Redis accordingly
        req_id = Red.incr('num_requests')
        print "This was request number", req_id

        # -- You can get all the data easily using form.data        
        req_dict = form.data
        print req_dict
        Red.set("request:{}".format(req_id), json.dumps(req_dict))
        get_back = json.loads(Red.get("request:{}".format(req_id)))
        print "Match?", get_back == req_dict
        print get_back

        # -- How many times was this animal requested?
        req_animal_cnt = Red.incr('animal-request:{}'.format(req_dict['name']))
        print "Animal '{}' has been requested {} times, including this time.".format(
            req_dict['name'], req_animal_cnt)

    else:
        if not form.submit.data:
            print 'No data was submitted'
        else:
            print 'Data was invalid'
            print 'Errors: {}'.format(form.errors)
                
    return render_template('request.html',form=form)


# Finally, let's add an admin-only page that summarizes requests. This
# will require us to (1) check to see that someone is logged in, (2)
# use Redis in a new way to grab the animal request information, and
# (3) present it in a new rendered template.
@app.route('/manage')
def manage():
    # first, if the user is not logged in, they need to go to the
    # login page. Normally, we would present more hints about why they
    # were redirected.
    if "username" not in session:
        return redirect(url_for('login'))

    # Now let's grab the relevant Redis information
    num_req = Red.get('num_requests')
    # Now grab all Redis keys of the form animal-request:* since these
    # represent the animal names that were requested
    requested_animals = list( Red.scan_iter(match="animal-request:*") )
    # --> this is now a list of keys, such as "animal-request:gerbil"
    # Next, grab the number of requests for each animal
    num_req_per_animal = [ Red.get(key) for key in requested_animals ]
    # Finally, put the information together
    num_req_dict = { ra[ra.find(':')+1:] : num
                         for ra,num in zip(requested_animals, num_req_per_animal) }
    # We can then send this to the admin web page to display.  Notice
    # in management.html how it makes use of session information even
    # though we did not need to pass it in. This is more Flask magic.
    return render_template('management.html', total=num_req,
                               by_animal=num_req_dict)

    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)


# In this version, we made two significant changes. First, we added a
# login mechanism so that the server can keep track of who logged in.
# Second, we added a special page that required being logged in to
# view it. This involved the new Redis method scan_iter. In this
# lesson, we'll make the logins better by storing usernames and
# passwords in Redis. Then, we'll add another table to the admin
# management page that shows the details of the requested animals.

# To Do 1: Improving the Login Mechanism
#
# 1. First we need to decide how usernames and passwords will be
#    stored in Redis.  Let's use the convention of
#    'password:<username>' giving the hash of the user's
#    username. (Hashing the password has the benefit that if someone
#    finds their password in the Redis server, they still can't log in
#    as them without finding a string that hashes to the same
#    value. But hashes are designed to make this cryptographically
#    hard.) Let's start by adding a username and password to the
#    server.  We can do this in an interactive Python session. Run the
#    following in Python. You can re-use this to add other
#    username-password pairs to the server.
'''
import redis
import hashlib
username = 'admin'
password = 'let-me-in'
Red = redis.StrictRedis()
key = 'password:{}'.format(username)
value = hashlib.md5(password).hexdigest()
Red.set( key, value )
print key, '-->', Red.get(key)
'''
# 2. Now, let's change how we check the credentials in the login
#    function.  Look up the username given in the form to get the md5
#    hex digest from Redis. Then compute the md5 hex digest from the
#    given password using something like
#        digest = hashlib.md5(password).hexdigest()
#    and be sure to add hashlib to the imports. Then only accept it
#    if the computed digest matchese the one retrieved from Redis.
#    Test this with various usernames and passwords.

# To Do 2: Improving the Management Display
#
# 3. We went through the troble of storing multiple fields when an
#    animal request was made. Now we want to show them to the
#    administrators. Just as we scanned keys of the form
#    "animal-request:*", we now want to scan keys of the form
#    "request:*". For each one, we then want to get the value. These
#    values need to be converted into dictionaries using json.loads.
#    Construct this and then print it to the server's terminal to make
#    sure you processed it right. It should look like a list
#    dictionaries. (You may need to submit some requests if you don't
#    have any.) Also, add that dictionary to what is passed to the
#    management template rendering.
#
# 4. Now go to management.html. After the table that is already there,
#    create a new similar table. The new one won't just have two
#    columns, but it will have five or six columns. We used iteritems
#    in the first table because by_animal was a dictionary. The new
#    data is a list of dictionaries, so you will want to use
#         {% for thing in thelist %}
#    like we did to make the fact list in the animal views. Bonus
#    points: use the dictsort "filter" on each dictionary to create
#    the table data elements, following the dictsort documentation in
#    http://jinja.pocoo.org/docs/dev/templates/#dictsort
#    Test it out.


