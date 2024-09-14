import smtplib
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

SESSMTPUSERNAME = os.environ.get('SMTP_USERNAME')
SESSMTPPASSWORD = os.environ.get('SMTP_PASSWORD')

smtp = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com")
smtp.connect("email-smtp.us-east-1.amazonaws.com", '587')
smtp.starttls()
smtp.login(SESSMTPUSERNAME, SESSMTPPASSWORD)

sender = "test@scholarscrape.com"
receivers = ["walker.alt.38552@gmail.com"]

# Secret key from Google reCAPTCHA (must be kept secure)
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        recaptcha_response = request.form.get('g-recaptcha-response')
        print(name, email, message, recaptcha_response)

        # Validate the form data
        if not all([name, email, message, recaptcha_response]):
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Verify reCAPTCHA with Google
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        print("recapthca key", RECAPTCHA_SECRET_KEY)
        recaptcha_payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        recaptcha_verification = requests.post(recaptcha_verify_url, data=recaptcha_payload)
        recaptcha_result = recaptcha_verification.json()
        print(recaptcha_result)

        if not recaptcha_result.get('success'):
            return jsonify({"status": "error", "message": "reCAPTCHA verification failed."}), 400

        # Proceed to send the email
        email_subject = f"Contact Form Submission"
        email_body = (f"""From: test from scholarscrape <test@scholarscrape.com>
To: caden <walker.alt.38552@gmail.com>
Subject: {email_subject}

                      Name: {name}
                      Email: {email}
                      Message: {message}
                      """)

        # Send email to each recipient
        while True:
            try:
                smtp.sendmail(sender, receivers, email_body)
                print("Successfully sent email")
                break
            except smtplib.SMTPException as e:
                print("Error", e)
                continue

        return jsonify({"status": "success", "message": "Submission received and emails sent!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
