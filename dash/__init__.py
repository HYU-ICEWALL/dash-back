#from flask import render_template

#    return render_template('index.html', name='World')
from flask import Flask, request, json, Response, make_response
from models import User
from database import db_session
app = Flask(__name__)

@app.route('/')
def root():
	if User().checkDup(request.args.get('id', '')) :
		return 'True'
	else:
		return 'False'

@app.route('/api/users', methods=['POST'])
def do_the_join():
	password = request.json['password']
	major = request.json['major']
	email = request.json['email']
	fb_id = request.json['fb_id']
	u = User(email, password, fb_id, major)	
	
	if ( u.checkDup(email) == True ) :
		return Response('', status=409)

	if ( len(password) == 0 or len(email) == 0 ):
		return Response('', status=400)
	
	db_session.add(u)
	db_session.commit()

	resp = make_response('', 201)
	resp.headers['Location'] = '/api/users/me'

	return resp

@app.route('/api/login', methods=['POST'])
def do_login():
	uname = request.form['email']
	password = request.form['password']
	u = User(uname, password)
	
	if ( u.checkLogin(uname, password) == True ) :
		resp = make_response('', 200)
		resp.headers['Location'] = '/api/users/me'
	else :
		resp = make_response('', 404)

	return resp
