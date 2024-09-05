import smtplib
import os

SESSMTPUSERNAME = os.environ.get('SMTP_USERNAME')
SESSMTPPASSWORD = os.environ.get('SMTP_PASSWORD')

smtp = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com")
smtp.starttls()
smtp.login(SESSMTPUSERNAME, SESSMTPPASSWORD)

sender = "test@scholarscrape.com"
receivers = ["walker.alt.38552@gmail.com"]
message = """From: Kate from Mailtrap <test@scholarscrape.com>
To: Noah Doe <timswei@gmail.com>
Subject: Check out my awesome email


This is my first email sent with Python using Mailtrap's SMTP credentials. WDYT?
"""
try:
    smtp.sendmail(sender, receivers, message)        
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print("Error", e)
    pass