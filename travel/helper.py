from django.core.mail import send_mail
from django.conf import settings  
from django.template.loader import render_to_string,get_template
from xhtml2pdf import pisa
import uuid
from django.http import HttpResponse

    
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
    
def save_pdf(params):
    response = HttpResponse(content='application/pdf')
    response['Content-Disposition'] = f'filename="{uuid.uuid4()}.pdf"'
    template = get_template('pdf.html')
    html = template.render(params)

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return None  # Return None if PDF generation fails

    # Get the PDF content from the response
    pdf_content = response.content

    return pdf_content