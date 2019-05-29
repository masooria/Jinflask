from flask import Flask, request, make_response, abort
from flask import render_template, url_for, session, redirect
from flask import flash

from flask_bootstrap import Bootstrap
from flask_moment import Moment

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from myData import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'zoolakataYamatarajabhanasalagam'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user (name):
    if check_db(name):
        # resp = make_response(f'<h1>namaste {name} </h1>')
        # resp.set_cookie('alm', '42')
        # resp.status_code = 301
        # print (resp.content_type)
        # print (url_for('user', name=name, _external=True))
        return render_template('user.html', name=name, items=items)
    else:
        abort(500)

@app.route('/dyn/<name>')
def dyn(name):
    name = name if check_db(name) else ""
    return render_template('user.html', name=name, items=items)

@app.route('/form', methods=['GET', 'POST'])
def form():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = form.name.data
        if old_name is not None and old_name != session.get('name'):
            flash('a name changer')
        session['name'] = form.name.data
        print (session.get('name'))
        return redirect(url_for('form'))
    return render_template('formin.html', form=form, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()