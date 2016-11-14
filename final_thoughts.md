# Final thoughts

This has been a quick tour to get you up to speed on making web
applications with Python, Flask, WTForms, Bootstrap, and
Javascript. There is a lot more to learn, but you now know enough to
hit the ground running. A list of follow-on topics are included
below. Also, since we ignored several important issues while speeding
through the example, these are listed below, too.

## Issues
* In our templates that used forms, we hard-coded in the action as,
  for example, "/request". These should all be filled in by the
  template using "{{ url_for(...) }}". That way if we change the URL
  (but leave the function name the same) then it will still work.
* When data is entered in the forms, we just use it as is. It would be
  a good idea to prepare the data before storing it. For example, we
  might fix or alter the capitalization in the animal names.
* In the animal creation page, we allow a maximum of six fun facts. It
  would be much better if the form allowed an arbitrary number of
  facts to be added.
* Most advanced web developers think in terms of three parts that are
  kept separate: presentation of the pages, logic of the server, and a
  data model. We did a fair job of keeping these separate by using
  Flask, Bootstrap, and Redis. However, our interaction with Redis is
  essentially "bare-handed" in that, for example, each time we query
  for an animal, we construct the key "animal:" + animal_name. This
  means that if we want to change it, we'll have a lot of places to
  find and fix. The better approach is to create one or more data
  model classes that provide methods for getting and storing
  data. This is pretty easy to do, but would have made Redis look more
  complicated than it really is, so we skipped it.
* The form validation errors are ungracefully handled by just putting
  them at the top as a list. They should show up next to the form
  inputs. This should be done using flash categories.


## Follow-On Topics
* After finishing the tutorial, the next thing you should do is try to
  create your own web application. Make it something you are genuinely
  interested in. Then, using the animal app as a reference, try to
  make it as good as you can. In the process, you'll run into lots of
  questions of the form "How do I ... with Flask, Bootstrap, or
  Javascript?". These questions can usually be answered by web
  searches.
* Redis is convenient and fast, but sometimes you are better off
  working with a regular relational database. How do you decide when
  to use a database?  How do you use one? How do you handle database
  connections? Which database should you use?
* Most programmers use libraries and frameworks to improve their
  Javascript. The most common library is JQuery. An important new
  framework is React. Learning how to use one or both of these is
  probably your quickest way to learn advanced skills.
