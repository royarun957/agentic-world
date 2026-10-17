import requests
import os
import smtplib
from email.message import EmailMessage
from crewai.tools import tool


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

@tool("Send Email")
def send_email(subject, text_body, html_body):
    """Send an email to the user
    Args:
        subject: The subject of the email
        text_body: The text body of the email
        html_body: The HTML body of the email
    Returns:
        True if the email was sent successfully, False otherwise
    """
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)

