#from flask import render_template

#    return render_template('index.html', name='World')
from flask import Flask, request, json, Response
from models import User
app = Flask(__name__)

@app.route('/')
def root():
	if User().checkDup(request.args.get('id', '')) :
		return 'True'
	else:
		return 'False'

@app.route('/api/users', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        return do_the_join()
    else:
		return 'ddd'
		
def do_the_join():
	password = request.json['password']
	major = request.json['major']
	email = request.json['email']
	fb_id = request.json['fb_id']
	u = User(email, password, fb_id, major)	
	
	if ( u.checkDup() == True ) :
		return Response('', status=401)

	if ( len(password) == 0 or len(email) == 0 ):
		return Response('', status=400)
	
	db_session.add(u)
	db_session.commit()

	resp = make_response('', status=201)
	resp.headers['Location'] = '/api/users/me'

	return resp
