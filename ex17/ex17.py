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
# 1. Bootstrap is enabled in your application by including a link to
#    it by adding the following link to the header of base.html:
'''
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
'''
#    Notice how adding this line changes the look of the web
#    site. Among other things, it changes the font, the link stylings,
#    the list styling, and the margins, giving it a more modern look.
#
# 2. Take a quick look a bootstrap cheat sheet, such as the one at
#    https://www.cheatography.com/masonjo/cheat-sheets/bootstrap/ or
#    https://bootstrapcreative.com/resources/bootstrap-3-css-classes-index/
#    and notice the wide range of options. These options are used by
#    putting an class tag in div elements. Let's start by reformatting
#    the navbar to make it have a solid background and be as wide as
#    the banner.
#
# 3. Next, pick a nice font.
#
# 4. Next, change the unordered list.
#
# 5. Put the number of times viewed in a badge.
#
# 6. Fix up the request page so that things line up nice and put it in
#    a jumbotron. Also fix up the login page.
#
# 7. Change the flash messages so they stand out more.
#
# 8. Change the edit and delete buttons to look snazzy. Fix the submit
#    buttons.
#
# 9. Put the animal image on the right for wide windows and below for
#    narrower windows. Fix the ordered list of fun facts to look
#    better (more spacing in between, bigger font). (Responsive design!)
#    If you have a smart phone, try viewing the site on your phone.
#
# 10. Fix the tables on the management page
#
# 11. Add a list of animals in a drop-down menu on the navbar.
#
# 12. Pick a color scheme for the page.
#
# 13. ?? Officially put the menu bar into the menu bar with the three lines?
#
# 14. Create a carousel of animal images (sized to the carousel)

'''
Next time with javascript:

Show how you can change things within the page. Rather than go to a
new page to delete a request, send the delete request by javascript,
cross out the line, and update the number in the badge.

Have the management page check for new requests periodically and then
update the lines as needed.

One more thing? Some mash-up with an API? Describe RESTful API
'''
