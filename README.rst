=========
fevent
=========

-------------------------------
E-commerce eventing system
-------------------------------

Setup requirements:
___________________

- python == v2.7.x
- pip >= 1.1
- `flask <http://flask.pocoo.org>`__ >= 0.8
- `flask-script <http://packages.python.org/Flask-Script/>`__ >= 0.3.1 (for shell commands support)
- `flask-sqlalchemy <http://packages.python.org/Flask-SQLAlchemy/>`__ >= 0.15
- `flask-mail <http://packages.python.org/flask-mail/>`__ >= 0.6.1
- `SQLAlchemy <http://www.sqlalchemy.org/>`__ >= 0.7.5
- `trafaret <http://github.com/deepwalker/trafaret>`__

Testing:
________

- `py.test <http://pytest.org>`__

Frontent development
____________________

We use `brunch.io <http://brunch.io>`__ for the client-side with `coffee-script <http://coffeescript.org>`__ and eco templates

================
Running project:
================

# At once setup virtualenv, next

./manage.py createall
./manage.py runserver
