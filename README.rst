Overview
========

I'm not sure this project is of interest for anyone but a few persons. This is mainly a WIP and a learning material

depends
=======

* django 1.3 beta
* django-extensions

basic setup
===========

I run and install in virtualenv as a unix user that has no other right.

Install::

% git clone git://github.com/feth/_noname.git
% cd _noname ; ./install #installs in ~/noname
% python ~/noname/namepoll/manage.py syncdb

Update::

%cd _noname ; git pull

Run::

% python ~/noname/namepoll/manage.py runserver 0.0.0.0:8080

(Replace 0.0.0.0 By 127.0.0.1 to listen on localhost only)

go in prod
==========

* remove DEBUG = True from settings.py
* python manage.py collectfiles
* set up a static files server that serves the static files
* use packed versions of jquery.js and jquery.ratings.js

translate
=========

Doc:
* http://docs.djangoproject.com/en/dev/topics/i18n/localization/
* http://docs.djangoproject.com/en/dev/topics/i18n/

Mark strings
------------

In code
~~~~~~~

All we need:

* '''ugettext_lazy''' for things that may be used more than once (ie. models)
* '''ugettext''' for strings to be translated immediately

*They* say we ought to import these functions "as _".

In templates
~~~~~~~~~~~~

Don't know yet.

In Javascript
~~~~~~~~~~~~

Don't know yet.

Update .po files
----------------

::

 cd _noname/namepoll/noname
 django-admin.py makemessages -l fr

Update .mo files
----------------

::

 django-admin.py compilemessages

