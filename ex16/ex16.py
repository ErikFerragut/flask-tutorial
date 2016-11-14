# Lesson 16 -- We add some advanced features to our web site

from animal_app import app
import os
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# In the last lesson, we overhauled the site, adding pages and links
# between them. In this session, we fill out the web site some more by
# (1) using flask's flash messages to give the user one-time
# information, (2) adding banner and favicon images, (3) creating an
# admin page where animals can be edited or added, and (4) including
# an ability to remove requests.
#
# 1. Use the flash messages. Flash messages are alerts to the user
#    that appear on the next page, but then don't appear again. We
#    will use these to say "You have successfully logged in" right
#    after a user logs in. Similarly, we will say "You have
#    successfully logged out." It will also be useful for giving
#    validation errors on the request form. To use flash messages, we
#    will need to import the module, pass the messages to the flash
#    functionality, and then grab and display those messages from
#    within a template.
#
#    a. In views.py we need to import flash from flask. This can go on
#       its own line or be combined with the "from flask import" line.
#
#    b. In the login route, change
#           print session["username"], "logged in!"
#       to
#           flash("Hello, {}, you have successfully logged in.".format(
#               session["username"]))
#
#    c. We want the messages to appear on whatever page is viewed next, so
#       we will add them to base.html. Put the following code in a block
#       just after the navbar block in base.html. It uses a template function
#       called get_flashed_messages() that is provided by the flash module.
'''
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
'''
#    d. Try it out. Log in and see if the message show up. We'll make
#       it look better in a future lesson.
#
#    e. Now add more messages for logging out and when an animal
#       request has been successfully added. Make sure it all works
#       like you wanted.
#
#    f. The last use of messages will be to show form validation
#       errors.  In request, rather than printing form.errors to the
#       terminal, create a loop that flashes each one to the
#       browser. Note that form.errors is a dictionary from the field
#       name to a list of strings. Did it work?
#
# 4. Two images, called banner.jpg and favicon.jpg, have been added in
#    the static directory. The banner is the image that appears at the
#    top of each page on the site. The favicon is the little icon that
#    appears next to the title in the tab.
#
#    a. Add the banner to base.html by inserting an html img tag
#       before the navbar. Put the image tag inside a <div> tag.
#
#    b. Note that when you get images for your site, you must make
#       sure you have the proper permissions or you could liable for
#       copyright violations. This banner was made by re-arranging an
#       image that itself was a composite of other images. The
#       original images and the composite were released under the
#       Creative Commons License meaning that they are free to use for
#       non-commercial use provided that proper attribution is
#       given. The attribution for these images have been put into a
#       template called credit.html. You need to add a link in the
#       footer to that page and create the route for it. This satisfies
#       the requirements of the license and avoids any legal issues.
#
#    c. The favicon is a special small image, usually 16x16 pixels and
#       sometimes in a special ico format. To serve it, add the
#       following line to the head of base.html. (The head is anywhere
#       before the body and generally includes links and the title.)
'''
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
'''
#       Visit the page with and without this link and verify that the
#       icon is used in at least one of the following ways: (1) next
#       to the tab, (2) when you favorite the page, (3) if you add the
#       page to your menu bar, and (4) next to the URL bar. (Most
#       browsers only use it in two or three of these ways.) (This icon
#       was found at http://www.favicon-generator.org/.)
#
# 5. Create an administration page where new animals can be added to the data
#    store.
#
#    a. Create a form in forms.py with input fields for each field
#       that we require for each animal. These are (1) animal name,
#       (2) source URL for the information, (3) up to 6 "fun facts",
#       (4) URL for an image, and (5) description of image. It also
#       needs a submit button. Add reasonable validators.
#
#    b. Create a template that extends base.html and presents the form
#       in the content block. You can compare to request.html.
#
#    c. Create a view for the form. The view must be only for logged
#       in users.  It should provide the form and then accept the
#       data. For now, just convert the animal information into a
#       dictionary and then into a JSON string and print it to the
#       server's terminal screen. You should now be able to test
#       5a, 5b, and 5c. You may want to just put in quick dummy information
#       to make sure it's working for now. When you are ready to really
#       add information, we've included blue-whale.txt with values for
#       the form.
#
#    d. Once you've got it printing out correctly, go ahead and store
#       the new data in the Redis data store. Keep in mind that Redis
#       will allow you to overwrite data without warning. Check that
#       it worked by going back to the index page (route '/') and
#       seeing if it's on the list of animals. If not, you probably
#       didn't use the right key for it; look at how we loaded the
#       data from JSON in ex10. If it is on the list, make sure the
#       new animal page renders correctly.
#
#    e. Add a link on the main page to the new add-an-animal page, but
#       make sure it only appears when someone is logged in.
#
# 6. It would be nice if administrators could just edit pages rather
#    than have to re-enter all of the information every time they want
#    to make a change.
#
#    a. Add a new route to the same view you used for adding new
#       animals, but now have it take an argument. Something like
#       '/edit/<animal>' would be appropriate. Note that the animal
#       argument must receive a default since it will not always be
#       passed in. We want '/add-animal' to be the main route, so it
#       must go last; put the new one before it.
#       
#    b. If the function receives an animal name, use that to look up
#       the animal in Redis. If it's not there, then just proceed as
#       before.  If it is there, then pre-populate the form by
#       assigning the values to, for example, form['name'].data or
#       form.name.data. Setting the facts list may be a bit
#       tricky. Make sure that form gets prepopulated when you visit
#       an existing animal and that it modifies the data correctly
#       when you submit.
#
#    c. Now that we can edit animals, let's avoid accidentally erasing
#       one. This could happen if someone adds an animal that already
#       exists.  When processing the new animal form, we want to
#       prevent it from overwriting an existing animal, but when we
#       edit one we do want it to overwrite. We could create two
#       different templates for editing and adding and have two
#       different functions, which is not a bad idea. Instead, we'll
#       use this opportunity to learn a new useful trick: a hidden
#       field. We've already used hidden fields for security. Here,
#       we'll use it to include more context within the form.
#
#       i. First, go to the new animal form and add a HiddenField
#       called "action". (You'll need to import HiddenField from
#       wtforms.)
#
#       ii. Then, in the add_animal view, set form.action.data to
#       either 'add' or 'edit' when the form is rendered, depending on
#       the route used to get to the function. You can get the route
#       with "request.url_rule.rule" after you import request from
#       flask. Now you tell if it's an add or an edit by looking at
#       form.action.data.
#
#       iii. Right after form.validate_on_submit(), check to see if
#       form.action.data is 'add'. If so, try to grab the record from
#       Redis. It will be None if it doesn't exist, in which case do
#       nothing. But if it is not None, then flash a message that you
#       cannot add an animal with the same name as an existing
#       animal. Then redirect to the edit page. Normally, this would be
#       redirect( url_for('add_animal', animal_name=form.name.data) ),
#       but that would go to the second url ('/add-animal'). You need
#       to pass "endpoint='edit_animal'" as an argument to the edit route,
#       and then redirect to the url for "edit_animal".
#
# 7. At this point, every animal has a well-defined edit URL. Use this
#    to add edit links next to each animal on the index page.  To make
#    it look nicer, have the link text be in an html button, like <a
#    href="..."><button>...</button></a>. While we're at it, there should
#    be edit buttons on the pages themselves, but they should only appear
#    if a user is logged in. (This last one is a bit tricky because,
#    currently, the Redis key is not sent to the animal.html template,
#    so you need to pass it in.)
#
# 8. As administrators add new animal pages, they will want to update
#    the list of requests on the admin page.
#
#    a. Create a view for the route '/delreq/<req_num>' that deletes
#       request number <req_num>. (Don't delete the animal record;
#       only the request.) Make sure the user is logged in before you
#       allow this. After this is done, redirect back to the
#       management page.
#
#    b. We had a counter of total requests. Let's keep that one, but
#       create a different one that is active requests. Increment it
#       each time a request is made. Decrement it each time a request
#       is deleted. Also, display it on the admin management page.
#       Since we started the number at zero even if you had requests
#       in Redis, the number will be off. Optional: Go into redis-cli
#       and set the number to the right value.
#
#    c. Add a delete button next to each request that will delete that
#       request if clicked. This is best done with a <button> element
#       inside an <a> element, as was done with the edit buttons.
#

