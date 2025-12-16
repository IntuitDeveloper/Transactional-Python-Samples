"""
Send a Single Email to a Single Recipient using Mandrill API

This script demonstrates how to send a single email to a single recipient
using the mailchimp_transactional Python library.

Usage:
    python email_with_single_recipient.py

Requirements:
    - mailchimp-transactional
    - python-dotenv

Install with:
    pip install mailchimp-transactional python-dotenv
"""

import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Mandrill API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

def send_email():
    """
    Send a single email to a single recipient using the Mandrill API.
    
    Returns:
        dict: Response from the Mandrill API
    """
    # Construct the message
    message = {
        'html': '<p>Hello HTML world!</p>',
        'text': 'Hello plain world!',
        'subject': 'Hello world',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'to': [{
            'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
            'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
            'type': 'to'
        }],
        'headers': {
            'Reply-To': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org')
        }
    }
    
    try:
        # Send the message
        response = mailchimp.messages.send({
            'message': message
        })
        
        print('Email sent successfully!')
        print('=' * 50)
        
        # Display the response details
        if response and len(response) > 0:
            result = response[0]
            print(f'Status: {result.get("status", "unknown")}')
            print(f'Email: {result.get("email", "N/A")}')
            print(f'Message ID: {result.get("_id", "N/A")}')
            
            if result.get('reject_reason'):
                print(f'Reject Reason: {result["reject_reason"]}')
        else:
            print(f'Unexpected result structure: {response}')
        
        print('=' * 50)
        return response
        
    except ApiClientError as error:
        print('Error sending email!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)
        return None

def send_email_with_advanced_options():
    """
    Send an email with advanced tracking and metadata options.
    
    Returns:
        dict: Response from the Mandrill API
    """
    message = {
        'html': '<p>Hello <strong>HTML</strong> world!</p>',
        'text': 'Hello plain world!',
        'subject': 'Advanced Email Test',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'to': [{
            'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
            'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
            'type': 'to'
        }],
        'headers': {
            'Reply-To': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
            'X-MC-Track': 'opens,clicks'
        },
        'important': True,
        'track_opens': True,
        'track_clicks': True,
        'auto_text': True,
        'auto_html': False,
        'inline_css': True,
        'tags': ['welcome', 'single-recipient', 'python'],
        'metadata': {
            'user_id': '12345',
            'campaign': 'welcome-series',
            'language': 'python'
        }
    }
    
    try:
        response = mailchimp.messages.send({
            'message': message
        })
        
        print('Advanced email sent successfully!')
        print('=' * 50)
        
        if response and len(response) > 0:
            result = response[0]
            print(f'Status: {result.get("status", "unknown")}')
            print(f'Email: {result.get("email", "N/A")}')
            print(f'Message ID: {result.get("_id", "N/A")}')
        
        print('=' * 50)
        return response
        
    except ApiClientError as error:
        print('Error sending advanced email!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)
        return None

if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('MANDRILL_API_KEY'):
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        exit(1)
    
    print('Sending basic email...')
    send_email()
    
    print('\n')
    
    # Uncomment to test advanced options
    # print('Sending email with advanced options...')
    # send_email_with_advanced_options()

