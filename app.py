import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

SESSMTPUSERNAME = os.environ.get('SMTP_USERNAME')
SESSMTPPASSWORD = os.environ.get('SMTP_PASSWORD')

sender = "test@scholarscrape.com"
recipients = ['timswei@gmail.com', 'walker.alt.38552@gmail.com']
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
        recaptcha_payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        recaptcha_verification = requests.post(recaptcha_verify_url, data=recaptcha_payload)
        recaptcha_result = recaptcha_verification.json()

        if not recaptcha_result.get('success'):
            return jsonify({"status": "error", "message": "reCAPTCHA verification failed."}), 400

        # Proceed to send the email
        email_subject = f"Contact Form Submission"

        msg = MIMEText(f"""                     
                    Name: {name}
                    Email: {email}
                    Message: {message}""")
        msg['Subject'] = email_subject
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        while True:
            try:
                smtp = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com")
                smtp.connect("email-smtp.us-east-1.amazonaws.com")
                smtp.starttls()
                smtp.login(SESSMTPUSERNAME, SESSMTPPASSWORD)
                smtp.sendmail(sender, recipients, msg.as_string())
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
