from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import secrets
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib  # Module for sending emails (consider secure alternatives)
import logging
from functools import wraps
from flask import request, redirect, url_for

logger = logging.getLogger(__name__)
load_dotenv()

class AuthManager:

    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    @staticmethod
    def hash_password(pwd):
        """
        Hashes a password using bcrypt.

        Parameters:
        pwd (str): The password to hash.

        Returns:
        str: The hashed password.
        """
        if not isinstance(pwd, str):
            print("Password must be a string")
            return
        if not pwd:
            print("Password cannot be empty")
            return
        
        try:
            encoded_pwd = pwd.encode()
            hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
            return hashed_pwd.decode()
        except Exception as e:
            logger.error(f"An error occurred while hashing the password: {e}")

    @staticmethod
    def validate_pwd(main_password, password):
        try:
            encoded_main_pwd = main_password.encode()
            encoded_pwd = password.encode()

            hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())

            # This function uses an approach designed to prevent timing analysis,
            # making it appropriate for cryptography.
            return secrets.compare_digest(hashed_pwd, encoded_main_pwd)
        except Exception as exc:
            logger.error(f'error checking password: {exc}')
            return False
    
    @staticmethod
    def create_confirmation_link(email=None, token=None):
        # generate link coupled with user token
        # 'confirm/<str:token>/<email>'
        base_url = 'http://localhost:5000/registration'
        confirmation_link = f'{base_url}/confirm/{token}'
        
        AuthManager.send_confirmation_email(email, confirmation_link)
    
    @staticmethod
    def send_confirmation_email(email, confirmation_link):
        # Replace with your email sender details and SMTP configuration
        sender_email = getenv('EMAIL')
        sender_password = getenv('EMAIL_PASSWORD')
        smtp_server = getenv('SMTP_SERVER')
        smtp_port = 465  # ssl port

        # print(sender_email)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "Registration Confirmation"

        # Create email body with the confirmation link
        body = f"Please click the link below to confirm your registration:\n{confirmation_link}"
        message.attach(MIMEText(body, "plain"))

        try:
            # Send email using Gmail's SMTP server
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                # server.starttls()  # Start TLS for encryption (consider secure alternatives)
                server.login(sender_email, sender_password)  # Replace with your credentials
                server.sendmail(sender_email, email, message.as_string())
                print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")
    
    @staticmethod
    def generate_jwt_token(username=None, user_id=None, email=None, registration=False, login=False):
        if email and registration and not username and not login and not user_id:
            try:
                payload = {
                    email: email,
                    'exp': datetime.now() + timedelta(days=3),  # expiration time
                    'iat': datetime.now(),  # issued at
                }

                token = jwt.encode(payload, AuthManager.JWT_SECRET_KEY, algorithm='HS256')
                return token
            except Exception as exc:
                logger.error(f'error generating registration token: {exc}')
                return
        
        if username and user_id and login:
            try:
                payload = {
                    user_id: user_id,
                    username: username,
                    'exp': datetime.now() + timedelta(minutes=3),  # expiration time
                    'iat': datetime.now(),  # issued at
                }
                token = jwt.encode(payload, AuthManager.JWT_SECRET_KEY, algorithm='HS256')
                return token
            except Exception as exc:
                logger.error(f'error generating login token: {exc}')
                return
    
    @staticmethod
    def verify_jwt_token(token=None, registration=None, login=None):
        try:
            payload = jwt.decode(token, AuthManager.JWT_SECRET_KEY, algorithm=['HS256'])
            if registration:
                return payload['email']
            if login:
                return payload['user_id'], payload['username']
        except jwt.ExpiredSignatureError as exc:
            logger.error(f'token expired: {exc}')
            return f'expired'
        except jwt.InvalidTokenError:
            logger.error(f'token invalid: {exc}')
            return f'invalid'
        except Exception as exc:
            logger.error(f'error verifying token: {exc}')
    
    @staticmethod
    def login_required(f):
        @wraps(f)
        def validated_token(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                print(f'token not found @login_required, redirecting to register')
                return redirect(url_for('authenticate.register'))
            user_id, username = AuthManager.verify_jwt_token(token=token, login=True)
            if not user_id or not username:
                print(f'id and username not found @login_required, redirecting to register')
                return redirect(url_for('authenticate.register'))
            return f(*args, **kwargs)
        return validated_token
