# -*- coding: utf-8 -*- 
#from flask import render_template

#    return render_template('index.html', name='World')
from flask import Flask, request, json, Response, make_response, abort, jsonify
from models import User
from database import db_session
from beaker.middleware import SessionMiddleware
from mail import sendmail
from conf import mailsubject
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
@app.route('/')
def root():
	return 'hello'

@app.route('/api/reset_password', methods=['POST'])
def resetPWD():
	email = request.form['email']
	u = User(email)
	status = u.resetPassword()
	
	if status['status'] == False:
		abort(404)

	pwd = status['password']
	try:
		fp = open('./dash/static/email.txt', 'rb')
		msg = str(fp.read())
		msg = msg.replace('[password]', pwd)

		sendmail(email, mailsubject, msg)
		db_session.commit()
	except:
		db_session.rollback()
		abort(500)
	return ''



@app.route('/api/users', methods=['POST'])
def do_the_join():
	try:
		password = request.json['password']
		major = request.json['major']
		email = request.json['email']
		fb_id = request.json['fb_id']
		u = User(email, password, fb_id, major)	
		
		if ( u.checkDup() == True ) :
			return make_response('', 409)
	
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
		resp = make_response('', 200)
		resp.headers['Location'] = '/api/users/me'
		session['user'] = u.getUser()
		session.save()
	else :
		abort(404)

	return resp

@app.route('/api/users/me', methods=['GET'])
def view_info():
	u = isLogin()
	if u == None:
		abort(404)
	
	return jsonify(u)


@app.route('/api/users/me', methods=['PUT'])
def modify_all():
	u = isLogin()

	if u == None:
		abort(404)

	try:
		session = request.environ['beaker.session']

		
		password = request.json['password']
		major = request.json['major']
		em = request.json['email']
		fb_id = request.json['fb_id']

		if u['email'] != em and User(em).checkDup() == True:
			return make_response('', 409)
		
		if User(u['email'], '', '', '', int(u['id'])).modify( { 'email' : em, 'password' : password, 'major' : major, 'fid' : fb_id } ) > 0 :
			
			resp = make_response('', 200)
			resp.headers['Location'] = '/api/users/me'
			u = User(em, password)
			u.checkLogin()
			session['user'] = u.getUser()
			session.save()
			db_session.commit()
			return resp
		else:
			db_session.rollback()
			abort(404)
	except:
		db_session.rollback()
		abort(400)
		
@app.route('/api/users/me', methods=['PATCH'])
def modify_part():
	u = isLogin()

	if u == None:
		abort(404)

	try:
		session = request.environ['beaker.session']

		if u['email'] != em and User(em).checkDup() == True:
			return make_response('', 409)
		
		if User(u['email'], '', '', '', int(u['id'])).modify( request.json ) > 0 :
			
			resp = make_response('', 200)
			resp.headers['Location'] = '/api/users/me'
			u = User(em, password)
			u.checkLogin()
			session['user'] = u.getUser()
			session.save()
			db_session.commit()
			return resp
		else:
			db_session.rollback()
			abort(404)
	except:
		db_session.rollback()
		abort(400)

@app.route('/api/users/me/delete', methods=['POST'])
def delUser():
	u = isLogin()
	
	if u == None:
		abort(404)
	
	u = User(u['email'], request.json['password'])
	print u.getUser()
	if ( u.checkLogin() == True ) :
		session = request.environ['beaker.session']
		print u.getUser()
		if ( u.delUser() == True):
			db_session.commit()
			session.delete()
			session.invalidate()
			return ''
		
	
	abort(404)

def isLogin():
	session = request.environ['beaker.session']
	
	if 'user' in session:
		u = session['user']
	else: 
		return None
		
	return u




