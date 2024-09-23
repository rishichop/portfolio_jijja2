from flask_login import LoginManager, login_user, login_required, logout_user
from flask import render_template, url_for, redirect, request, Blueprint, flash, session
from utils import bcrypt, login_manager, db
from datetime import datetime, timedelta
from user_model import Users
from forms import RegisterForm, OTPForm
from sms_service import send_sms
import random
import string

main_routes = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@main_routes.route("/")
def welcome():
    return redirect(url_for("main.register"))


@main_routes.route("/home")
@login_required
def home():
    return render_template("home.html")

@main_routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session["name"] = form.name.data
        session["email"] = form.email.data
        session["password"] = bcrypt.generate_password_hash(form.name.data).decode('utf-8')
        session["gender"] = form.gender.data
        session["branch"] = form.branch.data
        session["phone"] = form.phone.data

        if Users.query.filter_by(email=session.get("email")).first():
            flash('Email address already registered. Please use a different one or log in.')
            return redirect(url_for('main.login'))
        
        otp = ''.join(random.choices(string.digits, k=6))
        session["otp"] = otp

        send_sms(name=session.get('name'),
                 gender=session.get('gender'),
                 branch=session.get('branch'),
                 email=session.get('email'),
                 phone=session.get('phone'),
                 otp=session.get('otp'))

        return redirect(url_for('main.verify'))
    return render_template('register.html', form=form)

@main_routes.route("/verify", methods=['GET', 'POST'])
def verify():
    form = OTPForm()

    if form.validate_on_submit():
        if form.otp.data == session.get('otp'):
            user = Users(name=session.get('name'),
                         gender=session.get('gender'),
                         branch=session.get('branch'),
                         email=session.get('email'),
                         password=session.get('password'),
                         phone=session.get('phone'))
            
            db.session.add(user)
            db.session.commit()

            login_user(user)
            
            flash('OTP verified Successfully')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid OTP')
    return render_template('otp.html', form=form)