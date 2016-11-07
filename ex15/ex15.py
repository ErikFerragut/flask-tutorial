# Lesson 15 -- We make our web pages into a web site by connecting them up.

from animal_app import app
import os
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)

# To Do:
# 1. First familiarize yourself with how we've refactored the code. A
#    lot of changes were made. A short summary of what we did:
#
#         1. Turned the file into the animal_app package
#         2. Created views.py for the views
#         3. Created forms.py for the forms
#         4. Put static files (if any) in the static subdirectory
#         5. Moved all the templates into a subdirectory of animal_app
#         6. Created this file for running the server
#         7. Streamlined the templates so everything extends base.html
#         8. Use the site count for every view (not just animal)
#
#    Although all these changes did not change the site's behavior,
#    the organization will make it easier to continue growing the
#    site.
#
# 2. This site has a bunch of pages, but they don't actually connect
#    to each other.  We are now going to add a navigation list to the
#    base page so that you can get to any page from any other page.
#    In templates/base.html, as a block called navbar (a common
#    abbreviation for navigation bar) in the body. In it, place links
#    to the index (/), request, and login pages. Remember that these
#    links look like, for example,
#        <a href="{{ url_for('login') }}">Login</a>
#
# 3. Our index page is still not even a page! Create a short,
#    welcoming page by making a new template called index.html that
#    fills in the title and content blocks. Make it use the
#    session["username"] value using {{ session.username }}.
#
# 4. Modify the index page so that if the user is not logged in, it
#    recommends going to the login page and provides a link, but if
#    the user is logged in it recommends visiting the manage page and
#    provides that link.
#
# 5. Create a logout page according to the following steps. (A) Make a
#    form with nothing in it but a submit button, but change its
#    message from the default to "Log Out". (B) Create a view that
#    uses the form. If it was clicked, pop the username from the
#    session using session.pop("username"). Then redirect to the index
#    page. (C) Make sure the page can only be visited if the user is
#    logged in (see the management page for how that was done). If
#    they aren't logged in, redirect them to the index page.
