"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session, flash
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import User
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm

    
###
# Routing for your application.
###
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password_hash == form.password.data:
            login_user(user, form.remember_me.data)
            flash('Successfully logged in!')
            return redirect(request.args.get('next') or url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
    
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.before_request
def before_request():
    g.user = current_user
    


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
