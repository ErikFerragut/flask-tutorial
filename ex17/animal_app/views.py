import json, redis, hashlib
from forms import *
from flask import redirect, url_for, session, render_template, flash, request

from animal_app import app, Red


@app.route('/')
def hello():
    if session.get("username"):
        print "Seconds since login", Red.time()[0] - session["login time"][0]
    count = Red.incr('count')
    all_animals = [ f[f.find(':')+1:] for f in Red.scan_iter(match='animal:*') ]
    return render_template('index.html', num_views=count, all_animals=all_animals)


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
            flash("Hello, {}, you have successfully logged in.".format(
                session["username"]))

            return redirect(url_for('hello'))

        else:
            flash("Invalid login credentials.")
            print "Invalid credentials: username '{}' and password '{}'".format(
                form.username.data, form.password.data)
        
    elif form.submit.data:
        flash("Incomplete login form.")
        print "Username or password not supplied"

    count = Red.incr('count')
    return render_template('login.html', num_views=count, form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    if "username" not in session:
        return redirect(url_for('hello'))
    
    form = LogoutForm()
    if form.validate_on_submit():
        session.pop("username")
        flash("You have successfully logged out.")
        return redirect(url_for('hello'))

    count = Red.incr('count')
    return render_template('logout.html', num_views=count, form=form)


@app.route('/animal/<animal_name>')
def animal(animal_name):
    data_as_json = Red.get('animal:' + animal_name)

    if data_as_json is not None:
        data = json.loads(data_as_json)
        data['name'] = animal_name
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
        # Flash replaces debug information
        Red.incr('active-requests')
        flash("Animal '{}' has been requested, now for a total of {} times.".format(
            req_dict['name'], req_animal_cnt))

    else:
        if not form.submit.data:
            flash('No data was submitted')
        else:
            flash('Data was invalid')
            for field in form.errors:
                for error in form.errors[field]:
                    flash( field + ' - ' + error )

    count = Red.incr('count')
    return render_template('request.html',num_views=count,form=form)


@app.route('/manage')
def manage():
    if "username" not in session:
        return redirect(url_for('login'))

    # Now let's grab the relevant Redis information (shortened)
    num_req = Red.get('num_requests')
    num_req_dict = { key[key.find(':')+1:] : Red.get(key)
                     for key in Red.scan_iter(match="animal-request:*") }
    # We add the data from the requests
    req_detail = []
    for key in Red.scan_iter(match="request:*"):
        data = json.loads(Red.get(key))
        data['number'] = key[key.find(':')+1:]
        req_detail.append(data)

    # Also, management.html has been updated accordingly
    count = Red.incr('count')
    num_active = Red.get('active-requests')
    return render_template('management.html', num_views=count, total=num_req,
                               by_animal=num_req_dict, 
                               details=req_detail, total_active=num_active)

@app.route('/credits')
def credits():
    count = Red.incr('count')
    return render_template('credit.html', num_views=count)


@app.route('/edit/<animal_name>', endpoint='edit_animal')
@app.route('/add-animal', methods=['GET', 'POST'])
def add_animal(animal_name = None):
    if "username" not in session:
        return redirect(url_for('login'))  # require login

    form = NewAnimalForm()
    
    if form.validate_on_submit():
        key = "animal:" + form.name.data
        # Check for record overwrite in add-animal
        if form.action.data == 'add':
            print "Validated form for add-animal"
            get_it = Red.get('animal:' + form.name.data)
            print "get_it", get_it
            if get_it is not None:  # adding an animal that already exists
                flash('Cannot add {} because it already exist. Must edit instead.'.\
                          format(form.name.data))
                return redirect( url_for('edit_animal', animal_name=form.name.data) )
                
        # Otherwise, it's a new record or an edit of an existing, so update it.
        factlist = []
        for i in xrange(6):
            funfacti = 'funfact' + str(i+1)
            if funfacti in form.data and len(form[funfacti].data) >= 1:
                factlist.append( form[funfacti].data )
        
        data = { 'title':form.name.data,
                 'source_url':form.source_url.data,
                 'img_link': {"src":form.image_url.data,
                              "alt":form.image_desc.data},
                 'fact_list': factlist }

        Red.set(key, json.dumps(data))
        flash("Successfully added {}".format(form.name.data))
        return redirect(url_for('hello'))
    
    else:
        if animal_name is not None:  # editing
            get_it = Red.get('animal:' + animal_name)
            if get_it is not None:
                get_it_data = json.loads(get_it)
                form.name.data = get_it_data['title']
                form.source_url.data = get_it_data['source_url']
                form.image_url.data = get_it_data['img_link']['src']
                form.image_desc.data = get_it_data['img_link']['alt']
                for i, fact in enumerate(get_it_data['fact_list']):
                    form['funfact' + str(i+1)].data = fact
            else:
                flash('Animal {} is not in data store; cannot edit.'.format(animal_name))
                
    count = Red.incr('count')
    form.action.data = 'add' if request.url_rule.rule == '/add-animal' else "edit"
    print form.action.data
    return render_template('add_animal.html', num_views=count,
                               form=form)



@app.route('/delreq/<int:req_num>')
def delreq(req_num):
    Red.delete('request:' + str(req_num))
    Red.decr('active-requests')
    flash('Request {} deleted.'.format(req_num))
    return redirect( url_for('manage') )
