#!/usr/bin/python3
"""Flask mail"""
from flask_mail import Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'ranisminth@gmail.com'
SMTP_PASSWORD = 'wone dbrb oxpd czof'
SENDER_EMAIL = 'ranisminth@gmail.com'


def send_email(recipient_email, subject, body):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        server.quit()
        return True

    except SMTPAuthenticationError as e:
        return "Error Occurred"

