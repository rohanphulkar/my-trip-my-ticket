from django.core.mail import send_mail
from django.conf import settings  
from django.template.loader import render_to_string  

def send_password_reset_email(email,url):
    try:
        msg_plain = render_to_string('emails/email.txt',{'url':url})
        msg_html = render_to_string('emails/password_reset.html',{'url':url})
        subject = "Password reset request"
        send_mail(subject,msg_plain,settings.EMAIL_HOST_USER,[email],html_message=msg_html)
        return True
    except Exception as e:
        return False