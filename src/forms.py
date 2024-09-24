from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    gender = RadioField(label="Gender",
                             validators=[DataRequired()],
                             choices=["male", "Female", "Other"])
    branch = StringField("Branch", validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone no. (Please enter country code as well.)', validators=[DataRequired(), 
                                                                                    Regexp(r'^\+\d{1,3}\d{9,15}$', 
                                                                                           message="Invalid phone number. It must include a country code starting with '+'.")])
    submit = SubmitField('Get OTP through SMS')

class OTPForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')