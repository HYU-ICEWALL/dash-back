import flask from Flask

app = Flask(__name__)

@app.route('/')
def root():
	return 'h'

