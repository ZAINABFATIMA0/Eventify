from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decouple import config
from celery import shared_task

@shared_task
def send_otp_email(email, otp):
  
    html_message = render_to_string('otp_email.html', {'otp' : otp})   
    email = EmailMultiAlternatives(
        'Your OTP Code',
        "",
        config('EMAIL_HOST_USER'),
        [email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
