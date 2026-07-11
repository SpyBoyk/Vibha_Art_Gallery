from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_submission_email(subject, data):
    recipient = 'kalpeshkilje0296@gmail.com'
    message = f"New Form Submission: {subject}\n\n"
    for key, value in data.items():
        message += f"{key}: {value}\n"
    
    try:
        send_mail(
            subject=f"[Vibha Art Galleries] {subject}",
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@vibhaartgalleries.com'),
            recipient_list=[recipient],
            fail_silently=False
        )
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
