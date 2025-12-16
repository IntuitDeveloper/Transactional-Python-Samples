"""
Configuration module for Mailchimp Transactional Flask App.

Technical Documentation:
- Loads environment variables from a .env file using python-dotenv.
- Exposes key configuration values (API key, sender/recipient info) as module-level constants.
- Used throughout the app to securely access sensitive credentials and default email addresses.

User Documentation:
- Edit the .env file in the FlaskApp directory to set your Mailchimp API key and email addresses.
- These variables are automatically loaded and used by the application; no need to modify this file directly.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
DEFAULT_FROM_NAME = os.getenv('DEFAULT_FROM_NAME')
DEFAULT_TO_EMAIL = os.getenv('DEFAULT_TO_EMAIL')
DEFAULT_TO_NAME = os.getenv('DEFAULT_TO_NAME')

