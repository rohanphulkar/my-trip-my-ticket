from django.core.mail import send_mail
from django.conf import settings  
from django.template.loader import render_to_string  
import requests
from decouple import config
def send_password_reset_email(email,url):
    try:
        msg_plain = render_to_string('emails/email.txt',{'url':url})
        msg_html = render_to_string('emails/password_reset.html',{'url':url})
        subject = "Password reset request"
        send_mail(subject,msg_plain,settings.EMAIL_HOST_USER,[email],html_message=msg_html)
        return True
    except Exception as e:
        return False

# Load the SMS API key from environment variables
api_key = config("SMS_API_KEY")

def send_otp(phone_number,otp):
    try:
        # URL for sending OTP
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}"

        # send a get request to the url
        response = requests.get(url)

        # Return True if the response is successful
        return True
    except:
        #Return False
        return False