import re
from django.conf import settings
import os
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.hashers import make_password, check_password

def generate_random_token(size=64):
    raw_token=os.urandom(size).hex()
    return raw_token, make_password(raw_token)

def verify_token(token_from_user, current_token):
    return  check_password(token_from_user, current_token)

def get_identifier_type(text):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    phone_pattern = r"^(?:\+?\d{1,3}|\d{1,3}|0)\d{9}$"
    phone_no_country_pattern = r"^(0\d{9}|\d{9})$"
    username_pattern = r"^[a-zA-Z0-9_.]{3,20}$"
    if re.fullmatch(email_pattern, text):
        return "email"
    elif re.fullmatch(phone_pattern, text) or re.fullmatch(
        phone_no_country_pattern, text
    ):
        return "phone"
    elif re.fullmatch(username_pattern, text):
        return "username"
    return False


def validate_first_name(name):
    if not isinstance(name, str):
        return False, "Name must be a string."

    if not (2 <= len(name) <= 50):
        return False, "Name must be between 2 and 50 characters long."

    if not re.match(r"^[A-Za-z][A-Za-z\s\-\']*$", name):
        return (
            False,
            "first_name",
            "Name can only contain letters, spaces, hyphens, and apostrophes, and must start with a letter.",
        )
    return True, "Valid name."


def validate_last_name(name):
    if not isinstance(name, str):
        return False, "Name must be a string."

    if not (2 <= len(name) <= 50):
        return False, "Name must be between 2 and 50 characters long."

    if not re.match(r"^[A-Za-z][A-Za-z\s\-\']*$", name):
        return (
            False,
            "last_name",
            "Name can only contain letters, spaces, hyphens, and apostrophes, and must start with a letter.",
        )
    return True, "Valid name."


def validate_password(password):
    if not isinstance(password, str):
        return False, "Password must be a string."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, "password", "Valid password."


def validate_email(email):
    email_pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_pattern, email):
        return True, "Valid email."
    else:
        return False, "email", "Invalid email format."


def validate_username(username):
    username_pattern = r"^[a-zA-Z][a-zA-Z0-9._]{2,29}$"
    if re.match(username_pattern, username):
        return True, "Valid username."
    else:
        return False, "username", "Invalid username format."


def validate_phone_number(phone_number):
    phone_pattern = r"^\+?[1-9]\d{1,14}$"
    if re.match(phone_pattern, phone_number):
        return True, "Valid phone number."
    else:
        return False, "phone_number", "Invalid phone number format."


def validate_confirm_password(password, confirm_password):
    if password == confirm_password:
        return True, "Passwords match."
    else:
        return False, "confirm_password", "Passwords do not match."


def validate_profile_picture(file):
    if not file or file.name.split(".")[-1].lower() not in settings.ALLOWED_EXTENSIONS:
        return (
            False,
            "profile",
            "Invalid file extension. Only JPG, JPEG, PNG, and GIF files are allowed.",
        )

    file_size = len(file.read())
    if file_size > settings.PROFILE_IMAGE_SIZE:
        return False, "profile", "File size exceeds 2MB limit."
    file.seek(0)

    return True, "Valid profile picture."


def filter_error_list_item(list_item):
    if list_item:
        return list_item


def filter_validation_errors(validation_results: list) -> dict:
    print(validation_results)
    errors = [
        (error[1], error[2]) if error[0] == False and len(error)>2 else None
        for error in validation_results
    ]
    errors_dict = {}
    for error in errors:
        if error:
            errors_dict[error[0]] = error[1]
    return errors_dict



def send_password_reset_email(to_email, token):
    subject = "Reset Password"
    html_content = f"""
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Reset Password</title>
      </head>
      <body>
        <style>
          body {{
            display: flex;
            justify-content: center;
            flex-direction: column;
            align-items: center;
            font-size: medium;
            font-family: Verdana, Geneva, Tahoma, sans-serif;
          }}
          h1 {{
            color: dodgerblue;
          }}
          .reset_button {{
            background-color: dodgerblue;
            padding: 10px;
            border-radius: 10px;
            color: black;
            text-decoration: none;
            text-align: center;
            align-self: center;
          }}
          .reset_button:hover {{
            background-color: rgba(30, 143, 255, 0.253);
          }}
          footer {{
            background: #333;
            color: #fff;
            text-align: center;
            padding: 20px 0;
            position: relative;
            width: 100%;
            margin-top: 2rem;
          }}
        </style>
        <header>
          <h1>Reset Password</h1>
        </header>
        <main>
          <p>We have received your request to change password.</p>
          <p>
            If you have requested to change your password, click the link below, otherwise ignore.
          </p>
          <a href="{token}" target="_blank" class="reset_button">Reset password</a>
        </main>
        <footer>&copy; 2024 House Renting System Rwanda inc. All rights reserved.</footer>
      </body>
    </html>
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    email = EmailMessage(subject, html_content, from_email, recipient_list)
    email.content_subtype = "html"
    email.send()

def send_email_in_thread(to_email, token):
    email_thread = threading.Thread(
        target=send_password_reset_email, args=(to_email, token)
    )
    email_thread.start()