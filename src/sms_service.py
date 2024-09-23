from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()


def send_sms(name, gender, branch, email, phone, otp):
    client = Client(os.getenv('ACC_SID'), os.getenv('AUTH_TOKEN'))

    message = f"\nOTP: {otp},\nName: {name},\nGender: {gender},\nbranch: {branch},\nEmail: {email},\nPhone: {phone},"
    try:
        message = client.messages.create(
        from_=os.getenv('TWILIO_NUM'),
        body=message,
        to=phone
        )
    except:
        pass