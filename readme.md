I think you just need python 2.7+ and flask, which in turn requires some
things.

pip install flask

This repo is a tutorial for learning Flask, a web micro-framework
for Python. It is intended for use on Cloud 9 (c9.io) a cloud-based
IDE. The intended audience is High School students who have taken
an AP programming course or equivalent and have familiarity with
Python.

The tutorial will cover:
* Setting up and running Flask
* Creating views to handle urls
* Using templates for html rendering
* Storing data in either a json local file or on a local redis server
* Using bootstrap.js to format a web page
* Handling forms
* Using javascript for asynchronous updates
* Creating a scalable deployment


Part 1 is focused on server side programming (L1 -- L13)

Chapter 1 is on handling routes & providing views using Flask (L1-3)
* Add one or two links between pages and use url_for and redirect

Chapter 2 is on using templates (L4-7)

Chapter 3 is on data persistance using JSON and Redis (L8-10)

Chapter 4 is about handling forms (L11-12)

Chapter 5 is about sessions and logins (L13)

Intermission is about refactoring (L14) (Deployment prelude?)
* Breaking up your server files into static, templates, etc. 


Part 2 is focused on client side programming (L15 -- ?)

Chapter 6 is about connecting the pages by adding navigation bars, etc.
* What about changing the images to be on the server rather than
fetched?
* Or instead add a new image and make it local.

Chapter 7 is client side presentation with Bootstrap.js (ch ? through ?)

Chapter 8 is client side programming with javascript (ch ? through ?)
* Linking stuff with onclick and onhover & changing web page content
* Sending for more information from the server & using it


Part 3 is focused on systems engineering

Chapter 8 is deployment (ch ? through ?)
* Unit Testing & Load Testing & User Testing & A/B Testing
* Security concerns
* Monitoring performance & scalability
* Monetizing the results
* Connecting to other services (like google maps mash-ups)
* Running it from your home
* Migrating to AWS
* Making your code modular


Chapter 9 is a larger reference example in some detail


There organization is as follows:
1. Three top level Parts: server-side, client-side, and systems
2. Each Part is made up of about 4 to 5 Chapters
3. Each Chapter is made up of two to four core Lessons plus one or two
   Deep Lessons






* Issues
1. From ex2, Hello World! in hello() has a newline which is not an
   html newline. Maybe we should only return html?
2. There's no experience using url_for and redirect early on either in
   the python or the templates.
3. The images should be local so that results do not depend on other
   sites being up and active.

