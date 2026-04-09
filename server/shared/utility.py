# ========= PYTHON =========
import re
import threading

# ============== MODELS ==============
from users.models import AuthType

# ============== REST FRAMEWORK =========
from rest_framework.validators import ValidationError

# =============== DJNAGO ============
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

email_regex = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
phone_regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"


def check_user_input(input):
    if re.match(email_regex, input):
        return AuthType.VIA_EMAIL
    elif re.match(phone_regex, input):
        return AuthType.VIA_PHONE
    else:
        raise ValidationError(detail="email  or number is Invalid")


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        return self.email.send()


class Email:
    @staticmethod
    def send_email(data):

        email = EmailMessage(
            subject=data["subject"], body=data["body"], to=[data["email_to"]]
        )

        if data["content_type"] == "html":
            email.content_subtype = "html"
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        "email/verify_code.html", {"code": code, "to_email": email}
    )

    Email.send_email(
        {
            "subject": "Tastiqlash Kodi",
            "body": html_content,
            "content_type": "html",
            "email_to": email,
        }
    )
    
def validator_image_size(image):
    max_image_mb = 2

    if image.size > max_image_mb * 1024 * 1024:
        raise ValidationError(f"Image size must be lass than {max_image_mb}")
