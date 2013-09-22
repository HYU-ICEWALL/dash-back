from . import app
from database import db_session
from models import Major

from flask import request, json, Response, make_response, abort, jsonify


@app.route('/api/majors', methods=['GET'] )
def get_majors():
	m = Major().getMajors()
	
	print m
	return Response(json.dumps(m),  mimetype='application/json')
	