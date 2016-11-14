import json, redis, hashlib
from forms import *
from flask import redirect, url_for, session, render_template

from animal_app import app, Red


@app.route('/')
def hello():
    if session.get("username"):
        print "Seconds since login", Red.time()[0] - session["login time"][0]
        num_views = Red.incr('count')
        return 'Hello {}!<br/>{}<br/>{} site views'.format(
            session.get("username"), __file__, num_views)
    
    else:
        return 'Hello World!\n{}'.format(__file__)

    
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        given_password_hash = hashlib.md5(form.password.data).hexdigest()
        redis_key_for_hash = "password:" + form.username.data
        stored_password_hash = Red.get(redis_key_for_hash)
        if given_password_hash == stored_password_hash:
            # Successful login
            session["username"] = form.username.data
            session["login time"] = Red.time()
            print session["username"], "logged in!"

            return redirect(url_for('hello'))

        else:
            print "Invalid credentials: username '{}' and password '{}'".format(
                form.username.data, form.password.data)
        
    elif form.submit.data:
        print "Username or password not supplied"

    count = Red.incr('count')
    return render_template('login.html', num_views=count, form=form)


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

    count = Red.incr('count')
    return render_template('request.html',num_views=count,form=form,)


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
    count = Red.incr('count')
    return render_template('management.html', num_views=count, total=num_req,
                               by_animal=num_req_dict,
                               details=req_detail)

