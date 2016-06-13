from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect, url_for

import psycopg2
from psycopg2.extras import RealDictCursor
import json

flask_app = Flask('flaskapp')

@flask_app.route('/')
def index():
    return redirect('http://localhost:8095/liveview')

@flask_app.route('/liveview', methods=['GET', 'POST'])
def liveview():
    if request.method == 'GET':
        markers = json.dumps(getMarkers(), indent=2)
        if markers:
            print markers
            return render_template('mapscripts.html', markers=markers), 200
        return render_template('mapscripts.html'), 200
    else:
        # POST METHOD
        return render_template('mapscripts.html'), 200

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect('http://localhost:8095/liveview')

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=LiveView")

def getMarkers():
    """Get the list of markers from the database"""
    DB = connect()
    c = DB.cursor(cursor_factory=RealDictCursor)
    query = "SELECT id,name,latitude,longitude,link FROM Marker ORDER BY created DESC"
    c.execute(query)
    rows = c.fetchall()
    DB.close()
    return rows

app = flask_app.wsgi_app

