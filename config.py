import os
import logging

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///submissions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER') or 'default@example.com'  # Replace with a default or raise an error
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') or 'defaultpassword'  # Replace with a default or raise an error
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') or './uploads'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'document_uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}  # Add this line

    if not MAIL_USERNAME or not MAIL_PASSWORD:
        logging.error("EMAIL_USER and EMAIL_PASSWORD environment variables must be set.")
        raise ValueError("EMAIL_USER and EMAIL_PASSWORD environment variables must be set.")
    else:
        logging.info("Email configuration loaded successfully.")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        logging.info(f"Created upload folder at {UPLOAD_FOLDER}")
