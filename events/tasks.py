from celery import shared_task
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_registration_otp_email(email, otp, otp_expiry):
    html_message = render_to_string(
        'register_otp_email.html', 
        {'otp': otp, 'otp_expiry': otp_expiry}
    )   
    email = EmailMultiAlternatives(
        'Your OTP Code',
        "",
        config('EMAIL_HOST_USER'),
        [email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)


@shared_task
def send_unregistration_otp_email(email, otp, otp_expiry):
    html_message = render_to_string(
        'unregister_otp_email.html', 
        {'otp': otp, 'otp_expiry': otp_expiry}
    )   
    email = EmailMultiAlternatives(
        'Your OTP Code',
        "",
        config('EMAIL_HOST_USER'),
        [email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

@shared_task
def send_update_event_email(email, name, id):
    html_message = render_to_string(
        'event_updates_email.html', 
        {'name': name, 'event_id': id}
    )   
    email = EmailMultiAlternatives(
        'Event Updates',
        "",
        config('EMAIL_HOST_USER'),
        [email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
