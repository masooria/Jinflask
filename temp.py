from flask import Flask, request, make_response, abort
from flask import render_template, url_for

from flask_bootstrap import Bootstrap
from flask_moment import Moment

from datetime import datetime

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)

db = ['surya','teja', 'karna']
def check_db(name):
    if name in db:
        return True
    return False
items = ['milk','bread','biscuits']
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user (name):
    if check_db(name):
        resp = make_response(f'<h1>namaste {name} </h1>')
        resp.set_cookie('alm', '42')
        resp.status_code = 301
        print (resp.content_type)
        print (url_for('user', name=name, _external=True))
        return render_template('user.html', name=name, items=items)
    else:
        abort(500)

@app.route('/dyn/<name>')
def dyn(name):
    name = name if check_db(name) else ""
    return render_template('user.html', name=name, items=items)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()