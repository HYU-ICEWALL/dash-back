from flask import Flask, request, json, Response

app = Flask(__name__)

@app.route('/')
def root():
	return 'h'

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
	
	if ( len(password) == 0 or len(email) == 0 ):
		return Response('', status=400)
		
	return 'a'
