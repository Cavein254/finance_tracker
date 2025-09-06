from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_welcome_email(user_email):
    subject = "Welcome to Finance API 🚀"
    message = (
        "Hello!\n\n"
        "Thanks for registering with our Personal Finance API.\n"
        "You can now track your expenses, manage bills, and set budgets.\n\n"
        "Happy saving! 💰"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
