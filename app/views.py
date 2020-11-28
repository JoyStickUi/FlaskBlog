from app.app import app, db
from app.models import User, Role
from flask import render_template

@app.route('/')
def index():
	return render_template('index.html')

@app.errorhandler(404)
def handle_404(error):
	return render_template('errors/404.html', error=error), 404