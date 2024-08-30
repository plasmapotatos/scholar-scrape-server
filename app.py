from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') # Your email username
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = ('Timothy Wei', 'timswei@gmail.com')

# List of recipients
app.config['MAIL_RECIPIENTS'] = ['timswei@gmail.com']

mail = Mail(app)

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
        email_body = (f"Name: {name}\n"
                      f"Email: {email}\n"
                      f"Message:\n{message}")

        # Send email to each recipient
        for recipient in app.config['MAIL_RECIPIENTS']:
            msg = Message(subject=email_subject, recipients=[recipient], body=email_body)
            mail.send(msg)

        return jsonify({"status": "success", "message": "Submission received and emails sent!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
