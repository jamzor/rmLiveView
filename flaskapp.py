from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import redirect, url_for

flask_app = Flask('flaskapp')

@flask_app.route('/')
def index():
    return redirect(url_for('liveview'))

@flask_app.route('/liveview', methods=['GET', 'POST'])
def liveview():
    if request.method == 'GET':
        return render_template('mapscripts.html'), 200
    else:
        return render_template('mapscripts.html'), 200

@flask_app.route('/<path:path>')
def catch_all(path):
    return redirect('liveview')

app = flask_app.wsgi_app

