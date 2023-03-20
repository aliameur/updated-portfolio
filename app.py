from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
import smtplib

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


class ContactForm(FlaskForm):
    name = StringField('My name', [DataRequired()], render_kw={'placeholder': 'Full Name'})
    email = StringField('My email', [Email()], render_kw={'placeholder': 'name@example.com'})
    message = TextAreaField('My message', [DataRequired()],
                            render_kw={'placeholder': 'I want to say that...', 'rows': 5})


@app.route('/', methods=["GET", "POST"])
def home():
    form = ContactForm(request.form)
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            server_email = os.getenv('EMAIL')
            server_pass = os.getenv('PASSWORD')
            admin_email = os.getenv('ADMIN_EMAIL')
            connection.login(server_email, server_pass)
            connection.sendmail(from_addr=server_email,
                                to_addrs=admin_email,
                                msg="Subject: New Message From Personal Website\n\n"
                                    f"Name: {form.name}\n"
                                    f"Email: {form.email}\n"
                                    f"Message: {form.message}\n")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
