import smtplib
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

SESSMTPUSERNAME = os.environ.get('SMTP_USERNAME')
SESSMTPPASSWORD = os.environ.get('SMTP_PASSWORD')

smtp = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com")
smtp.starttls()
smtp.login(SESSMTPUSERNAME, SESSMTPPASSWORD)

sender = "test@scholarscrape.com"
receivers = ["walker.alt.38552@gmail.com"]

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get data from the form
        print(request.form)
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate the form data
        if not all([name, email, message]):
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Create the email message
        email_subject = f"Contact Form Submission"
        email_body = (f"""From: test from scholarscrape <test@scholarscrape.com>
To: caden <walker.alt.38552@gmail.com>
Subject: {email_subject}

    
                      Name: f{name}
                      Email: f{email}
                      Message: f{message}
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
