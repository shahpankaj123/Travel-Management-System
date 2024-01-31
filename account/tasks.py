from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import EmailMessage

from bus_reserve.models import TicketOrder

@shared_task
def send_activation_email(recipient_email, activation_url):
    subject = 'Activate your account on '
    from_email = settings.EMAIL_HOST_USER
    to = [recipient_email]
    html_content = render_to_string('account/activation_email.html', {'activation_url': activation_url,'topic':'Activation Mail','desc':'Youre receiving this email because you need to finish activation process.'})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

@shared_task
def send_mail_verify(email,token,token1):
    subject = 'Your account to be verified to Reset Password'
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    html_content = render_to_string('account/activation_email.html', {'activation_url': token,'topic':'Token Veified Mail','desc':f'Your Token Verified Number-{token1}'})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
 
@shared_task
def Send_ticket(request):
    print(request)
    orders = TicketOrder.objects.filter(user_id__email=request[0],\
                                        ticket_id__schedule_id=request[1]).order_by('-bought_date')[0]
    print(orders)
    template = get_template('account/ticket.html')
    html_content = template.render({'context': orders})

    pdf_data = BytesIO()
    
    pisa.CreatePDF(html_content, dest=pdf_data)

    response = HttpResponse(pdf_data.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="document.pdf"'

    subject = 'PDF Attachment'
    message = 'Please find the attached PDF document.'
    from_email = settings.EMAIL_HOST_USER
    to_email = request[0]

    email = EmailMessage(subject, message, from_email, [to_email])
    email.attach('document.pdf', response.content, 'application/pdf')
    email.send()

@shared_task
def send_refund_mail(tik_id):
    subject = 'Refund request'
    message = f'Ticket id {tik_id} is asking for refund'
    from_email = settings.EMAIL_HOST_USER
    to_email = 'aaryanshah651@gmail.com'

    EmailMessage(subject, message, from_email, [to_email]).send()