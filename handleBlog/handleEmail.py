import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from django.core.mail import send_mail
from django.conf import settings
from . models import *

def sendForgetPassMail(userEmail, token):

    user = CustomUser.objects.get(userEmail=userEmail)

    try:
        subject = "Your forget password link"
        message = "Hi"
        # message = f"Hi {user.userName},\n\nPlease click on the following link to reset your password:\n\nhttp://127.0.0.1:8000/resetPassword/{token}\n\nIf you did not make this request, please ignore this email and your password will remain unchanged.\n\nRegards,\nYudiz"
        from_email = settings.EMAIL_HOST_USER
        print("fromEmail--", from_email)
        recipient_list = (userEmail,)
        print("receiverList--", recipient_list)
        send_mail(subject, message, from_email, recipient_list)    
        print("Please")
        return True
    except Exception as e:
        print("python --- ", e)
        # Handle case where user with given email does not exist
        # For example, you can log an error,

  