# Lesson 15 -- We make our web pages into a web site by connecting them up.

#
# To Do:
# 1. Create a file called forms.py and move all of the forms into that
#    file. It will need to import FlaskForm, the validators, and the
#    field types. In this file, you should remove those imports, but
#    add an import for the newly created file. Make sure the server
#    still works.
#
# 2. Create another file and call it views.py. Now move all of the
#    views into that file. It will also need some imports, which can
#    then be removed from this file (unless it still uses it). Add an
#    import for the new file to this file. Test it again to make sure
#    you didn't break it.
#
# 3. We were not very careful with how we used the templates to make
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



Red = redis.StrictRedis()
app = Flask(__name__)
app.secret_key = hex(random.randrange(1<<128))  # 128 bits of randomness


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
    data_as_json = Red.get(animal_name)

    if data_as_json is not None:
        data = json.loads(data_as_json)
        count = Red.incr('count')
        return render_template('animal.html', num_views=count, **data)
    else:
        return "Oops, I don't know about {}".format(animal_name)

    
@app.route('/request', methods=['post', 'get'])
def request():
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
# 1. First familiarize yourself with how we've refactored the code. Does it
#    look like how you did it in the last lesson? Notice that we also added some
#    comments to the classes and functions.

