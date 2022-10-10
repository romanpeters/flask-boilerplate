from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy.orm.exc import NoResultFound
from app.models import database, forms
from app import app, sqlalchemy

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        query = database.User.query.filter_by(username=username)

        try:
            user = query.one()
            if not user.check_password(password):
                flash("Wrong password")
                return render_template('index.html', form=login_form)
        except NoResultFound:
            flash("User not found")
            return redirect(url_for('register'))

        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        # if not is_safe_url(next):  # todo
        #     return flask.abort(400)
        return redirect(next or url_for('index'))
    else:
        print("not valid")
    return render_template('login.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = database.User(username=username)
        user.set_password(password)
        sqlalchemy.session.add(user)
        sqlalchemy.session.commit()
        flash("Created account")
        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))
