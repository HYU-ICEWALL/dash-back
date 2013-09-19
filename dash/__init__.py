# -*- coding: utf-8 -*- 
#from flask import render_template

#    return render_template('index.html', name='World')
from flask import Flask, request, json, Response, make_response, abort, jsonify
from models import User
from database import db_session
from beaker.middleware import SessionMiddleware

session_opts = {
	'session.type' : 'ext:memcached',
	'session.url' : '127.0.0.1:11211',
	'session.data_dir' : './cache'
}

app = Flask(__name__)
app.secret_key = "/D/s)8'~!>W$%914<S_T#7)8Q8O(|i"
app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)

@app.route('/')
def root():
	return 'hello'

@app.route('/api/users', methods=['POST'])
def do_the_join():
	try:
		password = request.json['password']
		major = request.json['major']
		email = request.json['email']
		fb_id = request.json['fb_id']
		u = User(email, password, fb_id, major)	
		
		if ( u.checkDup() == True ) :
			abort(409)
	
		if ( len(password) == 0 or len(email) == 0 ):
			abort(400)
	
		db_session.add(u)
		db_session.commit()

		resp = make_response('', 201)
		resp.headers['Location'] = '/api/users/me'

		return resp

	except:
		abort(400)


@app.route('/api/login', methods=['POST'])
def do_login():
	uname = request.form['email']
	password = request.form['password']
	u = User(uname, password)
	
	if ( u.checkLogin() == True ) :
		session = request.environ['beaker.session']
		print session
		resp = make_response('', 200)
		resp.headers['Location'] = '/api/users/me'
		session['user'] = u.getUser()
		session.save()
		print session
	else :
		abort(404)

	return resp

@app.route('/api/users/me', methods=['GET'])
def view_info():
	u = isLogin()
	
	if u == None:
		abort(404)
	
	return jsonify(u)





def isLogin():
	session = request.environ['beaker.session']
	
	if 'user' in session:
		u = session['user']
	else: 
		return None
		
	return u




