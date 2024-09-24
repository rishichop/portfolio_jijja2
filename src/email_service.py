from .utils import mail
from flask_mail import Message
import os
from dotenv import load_dotenv
load_dotenv()

def contact_email(name, email, message):
    msg = Message('Portfolio Contact', sender="noreply@demo.com", recipients=[os.getenv('EMAIL_USER')])
    msg.body = f'Name = {name}\n Email = {email}\n Message = {message}'
    mail.send(msg)