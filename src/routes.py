from flask_login import login_user, login_required, logout_user
from flask import render_template, url_for, redirect, Blueprint, flash, session
from .utils import bcrypt, login_manager, db
from datetime import datetime, timedelta
from .user_model import Users
from .forms import RegisterForm, OTPForm, LoginForm, ContactForm
from .sms_service import send_sms
from .email_service import contact_email
from .portfolio_info import resume
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
    data = resume
    return render_template("home.html", data=data)

@main_routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session["name"] = form.name.data
        session["email"] = form.email.data
        session["password"] = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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
            
            flash('OTP verified Successfully')
            return redirect(url_for('main.login'))
        else:
            flash('Invalid OTP')
    return render_template('otp.html', form=form)

# @main_routes.route("/about")
# def about():
#     return render_template("about.html")

@main_routes.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        contact_email(name, email, message)
        flash("Email Sent Successfully!")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)

@main_routes.route("/logout")
def logout():
    logout_user()
    flash("Logout Successful.")
    return redirect(url_for("main.login"))

@main_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.home'))
            
            else:
                flash('Incorrect password!')
                return redirect(url_for("main.login"))

        else:
            flash('User Not Found. Please Register!')
            return redirect(url_for("main.login"))

    return render_template('login.html', form=form)