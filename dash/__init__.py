# -*- coding: utf-8 -*- 
#from flask import render_template

#    return render_template('index.html', name='World')
from flask import Flask
from beaker.middleware import SessionMiddleware

from methodover import HTTPMethodOverrideMiddleware
session_opts = {
	'session.type' : 'ext:memcached',
	'session.url' : '127.0.0.1:11211',
	'session.data_dir' : './cache'
}

app = Flask(__name__)
app.secret_key = "/D/s)8'~!>W$%914<S_T#7)8Q8O(|i"
app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)


import userc
import majorc