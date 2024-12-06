from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/visits')
def visits():
    return render_template('visits.html')


