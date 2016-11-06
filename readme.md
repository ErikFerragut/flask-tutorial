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

Unit 1 is mainly server side programming with Flask (ex 1 through 7)
* Add links between pages

Unit 2 is data persistance using JSON and Redis (ex 8 through 10)

Unit 3 is about handling forms
* Add handling forms, possibly as a new Unit?

Unit 4 is about sessions and logins
* Add logins and passwords and so on

Unit 5 is client side presentation with Bootstrap.js (ex ? through ?)
* Breaking up your server files into static, templates, etc.

Unit 6 is client side programming with javascript (ex ? through ?)
* Linking stuff with onclick and onhover & changing web page content
* Sending for more information from the server & using it

Unit 7 is usability
* Add routes, such as animals to the view for animal
* convert the animal name to lower case

Unit 8 is deployment (ex ? through ?)
* Testing -- how do you do this on cloud9?
* Migrating to aws
* Running it from home

Unit 9 is a larger example in some detail
