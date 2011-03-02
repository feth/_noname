Overview
--------

I'm not sure this project is of interest for anyone but a few persons. This is mainly a WIP and a learning material

depends
-------

* django-ratings https://github.com/dcramer/django-ratings (ou PyPI)
* django 1.3 beta

basic setup
-----------

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

