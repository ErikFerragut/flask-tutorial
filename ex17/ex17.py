# Lesson 17 -- We use Bootstrap to improve the site's appearance

from animal_app import app
import os
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# HTML, the language for web pages, is a way to describe the pieces of
# a page. The styling of those pieces can be done in HTML, but we have
# avoiding doing so because it is better to do the styling with CSS, a
# different language that controls formatting. CSS can get somewhat
# complicated because it is essentially a long list of options. For
# this reason, software engineers have developed frameworks that
# simplify the display of web pages. One of the most popular such
# frameworks was created by people at Twitter and is called Bootstrap.
#
# Many good tutorials are available online for Bootstrap, so we only
# cover the main ideas here:
#
# 1. Bootstrap can be enabled in your application by including links
#    to where it is on the internet, which can often lead to faster
#    load times for users. However, since we'll be mostly running it
#    on the same machine as the server, it will be easier and faster
#    to put the files in static and include them with:
'''
<link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='jquery.min.js') }}"></script>
<script src="{{ url_for('static', filename='bootstrap.min.js') }}"></script>
'''
#    The first link includes a CSS file and the second and third
#    include Javascript files. Notice how adding these lines change
#    the look of the web site. Among other things, it changes the
#    font, the link stylings, the list styling, and the margins,
#    giving it a more modern look.
#
# 2. Take a quick look a bootstrap cheat sheet, such as the one at
#    https://www.cheatography.com/masonjo/cheat-sheets/bootstrap/ or
#    https://bootstrapcreative.com/resources/bootstrap-3-css-classes-index/
#    and notice the wide range of options. These options are used by
#    putting an class tag in div elements. Let's start by reformatting
#    the navbar to make it have a solid background and be as wide as
#    the banner.
#
#    a. Go to base.html and place the navbar links inside of a <nav> HTML
#       element. This element is new in HTML5. We want the nav element to
#       be recognized by Bootstrap as the default navbar:
#             <nav class="navbar navbar-default">...</nav>
#       It is common with Bootstrap to have multiple classes. This puts
#       a gray box around the navbar items. (Notice how the bar extends
#       beyond the banner... We'll fix this later.)
#
#    b. Now, rather than just giving the three links, we'll put them in
#       an unordered list and mark them as navbar items so that Bootstrap
#       can format them nicely. Enclose the links inside of:
#             <ul class="nav navbar-nav"> ...  </ul>
#
#    c. Put each link in its own list item <li class="nav-item">
#       ... </li>. Also add a class="nav-link" to each anchor <a>
#       element.
#
# 3. Bootstrap allows you to make messages that hover when you put the
#    mouse over something. Perhaps the link name "Request" is
#    unclear. Let's add a message that says the link is for requesting
#    additional animals for the web page. Inside the anchor <a>
#    element, add the following fields: data-toggle="tooltip"
#    data-placement="bottom" title="Request an animal to add to the
#    website". These fields go after "<a" and before ">". The new
#    fields can go either before or after the href field.
#
# 4. With Bootstrap, it is easy to make drop-down menus in the navigation
#    bar. So we'll add a drop down of animals. Let's put it right after
#    Index and before Request.
#
#    a. Add a new list item:
#           <li class="nav-item dropdown"> ... </li>
#
#    b. Inside that list item put in a non-effective link with a
#       "button" role with:
#           <a class="nav-link dropdown-toggle" data-toggle="dropdown"
#              href="#" role="button" aria-haspopup="true" aria-expanded="false">
#           ... </a>
#       The aria-haspopup and aria-expanded tell the browser extra information
#       about the element that makes it easier for people with disabilities
#       to view the page.
#
#    c. Inside that anchor element, just write the word "Animals" followed by
#       <b class="caret"></b>, which puts a symbol that suggests there's a menu
#       under the word.
#
#    d. The actual drop down elements go underneath, in <div> element within the
#       same <li> element. Let's first add a placeholder:
#           <ul class="dropdown-menu">
#              <li><a class="dropdown-item" href="#">Drop 1</a></li>
#              <li><a class="dropdown-item" href="#">Drop 2</a></li>
#           </ul>
#       We can't put the actual animals in because they need to be passed
#       into the template. We'll do this in the next step. For now, just make
#       sure the drop down works.
#
# 5. One problem with putting the animals in the list is that this
#    list will be in base.html, which is part of every page. So you
#    might think we need to compute the list in every view and pass it
#    to the template. Luckily, Flask offers an easier way. We can put
#    it into a global dictionary and then access that from every
#    template.
#
#    a. Create a special function that will be called at the beginning
#       of each user's interaction with the server. This is where an
#       "application context" is first available, which is what we need
#       if we want to store things in the global g. The function should
#       look like:
'''
@app.before_request
def set_up_animal_dict():
    g.all_animals = sorted([ f[f.find(':')+1:]
                             for f in Red.scan_iter(match='animal:*') ])
'''
#       This is the same code we used to make the list of animals in
#       the index, except now we are sorting it.
#
#    b. In views.py, import g from flask.
#
#    c. Replace the placeholder list items in the dropdown menu with
#       a template for loop that runs over each animal in g.all_animals.
#       For each animal, add a link. Test it out.
#
# --HERE--
# 6. Put the number of times viewed in a badge.
#
# 7. Change the edit and delete buttons to look snazzy. Fix the submit
#    buttons.
#
# -- Split into >1 lessons
#
# 8. Use the grid system
#
# 9. Put the animal image on the right for wide windows and below for
#    narrower windows. Fix the ordered list of fun facts to look
#    better (more spacing in between, bigger font). (Responsive design!)
#    If you have a smart phone, try viewing the site on your phone.
#
# 10. Fix up the request page so that things line up nice and put it in
#     a jumbotron. Also fix up the login page.
#
# 11. Fix the tables on the management page
#
# -- Split into >1 lessons
#
# 12. Next, change the unordered list. To a list of media items?
#
# 13. Change the flash messages so they stand out more.
#
# 14. Create a carousel of animal images (sized to the carousel)
#
# 15. Customize: color scheme & font
#

'''
Next time with javascript:

Show how you can change things within the page. Rather than go to a
new page to delete a request, send the delete request by javascript,
cross out the line, and update the number in the badge.

Have the management page check for new requests periodically and then
update the lines as needed.

One more thing? Some mash-up with an API? Describe RESTful API
'''
