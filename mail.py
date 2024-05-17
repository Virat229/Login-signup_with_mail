import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random

SENDGRID_API_KEY = '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'


def send(val, recipient_email_tuple):
    sender_email = "gargvirat5@gmail.com"
    subject = "OTP"
    if recipient_email_tuple:
        recipient_email = recipient_email_tuple[0]
        body = f"This is a test email sent from Grow Tech. Your OTP to sign in is {val}"
        message = Mail(
            from_email=sender_email,
            to_emails=recipient_email,
            subject=subject,
            plain_text_content=body)
        try:
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(message)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    else:
        print("No recipient email found")

