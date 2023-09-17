from django.core.mail import send_mail
from django.conf import settings  
from django.template.loader import render_to_string  
    
def send_booking_confirmation_email(context):
    try:
        msg_plain = render_to_string('emails/booking_confirmed.txt',context)
        msg_html = render_to_string('emails/booking_confirmed.html',context)
        subject = "Your booking has been confirmed."
        email_sent =send_mail(subject,msg_plain,settings.EMAIL_HOST_USER,[context['email']],html_message=msg_html)
        print(email_sent)
        return True
    except Exception as e:
        print(e)
        return False

def send_booking_cancellation_email(context):
    try:
        msg_plain = render_to_string('emails/booking_cancel.txt',context)
        msg_html = render_to_string('emails/booking_cancel.html',context)
        subject = "Your booking has been cancelled."
        email_sent=send_mail(subject,msg_plain,settings.EMAIL_HOST_USER,[context['email']],html_message=msg_html)
        print(email_sent)
        return True
    except Exception as e:
        
        return False