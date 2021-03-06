# Main Blueprint. This Blueprint will hold all routes
# that are part of the 'main' website interface, that
# teachers and visitors access

from flask import Blueprint, current_app
from teachersapp import db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from teachersapp.main.forms import RegistrationForm, LoginForm
from teachersapp.models import User, Language, TeachingProfile
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template(
        'home.html', 
        map_key=current_app.config['GOOGLE_MAPS_API_KEY']
    )

@main.route("/catalog")
def catalog():
    languages = Language.query.all()
    selected_lang_id = request.args.get('lang', default=1, type=int)
    selected_lang = next(x for x in languages if x.id == selected_lang_id)

    return render_template(
        'catalog.html', 
        languages=languages, 
        selected_lang=selected_lang
    ) 

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'You have logged out!', 'success')
    return redirect(url_for('main.home'))       

@main.route("/register", methods=['GET', 'POST'])
def register():
    # Sanity check: if the user is already authenticated then go back to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Otherwise process the RegistrationForm from request (if it came)
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash user password, create user and store it in database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.username.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()

            flash(f'Account created for: {form.username.data}!', 'success')
            return redirect(url_for('main.home'))
        except IntegrityError:
            flash(f'Could not register! The entered username or email might be already taken', 'danger')
            print('IntegrityError when trying to store new user')
            db.session.rollback()
        
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    # Sanity check: if the user is already authenticated then go back to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)