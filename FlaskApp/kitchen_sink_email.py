"""
Kitchen Sink - Comprehensive Email with All Features

This script demonstrates a comprehensive Mailchimp Transactional (Mandrill)
message exercising many available settings in one example.

Usage:
    python kitchen_sink_email.py

Requirements:
    - mailchimp-transactional
    - python-dotenv
"""

import os
import base64
from datetime import datetime, timedelta
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))


def read_file_as_base64(file_path):
    """Helper to read a local file and return a Base64 string."""
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        return None


def send_kitchen_sink():
    """
    Send a comprehensive email demonstrating all major Mandrill features.
    """
    # Prepare attachments
    attachments = []
    sample_pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
    if os.path.exists(sample_pdf_path):
        pdf_content = read_file_as_base64(sample_pdf_path)
        if pdf_content:
            attachments.append({
                'type': 'application/pdf',
                'name': 'sample.pdf',
                'content': pdf_content
            })

    # Inline images (empty for this demo)
    images = []

    # Complete Mandrill message with ALL features
    message = {
        # Basic content
        'html': '''
            <h1>Hello {{fname}}!</h1>
            <p>This email demonstrates multiple Transactional API features.</p>
            <p><strong>Company:</strong> {{company_name}}</p>
            <p><strong>Account:</strong> {{account_id}}</p>
            <div style="width: 50px; height: 50px; background: #007bff; border: 2px solid #0056b3; display: inline-block;"></div>
            <p>This is a comprehensive demonstration of the Mandrill API capabilities in Python.</p>
        ''',
        'text': '''Hello {{fname}}!

This email demonstrates multiple Transactional API features.
Company: {{company_name}}
Account: {{account_id}}

This is a comprehensive demonstration of the Mandrill API capabilities in Python.
        ''',

        # Basic fields
        'subject': 'Hello {{fname}} - Mandrill Features Demo',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),

        # All recipient types
        'to': [
            {
                'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
                'type': 'to'
            }
        ],
        # Uncomment to add CC and BCC recipients
        # 'cc': [
        #     {'email': 'cc@example.com', 'name': 'CC User', 'type': 'cc'}
        # ],
        # 'bcc': [
        #     {'email': 'bcc@example.com', 'name': 'BCC User', 'type': 'bcc'}
        # ],

        # Headers
        'headers': {
            'Reply-To': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
            'X-Custom-Header': 'Mandrill-Demo-Python'
        },

        # Merge variables
        'global_merge_vars': [
            {'name': 'company_name', 'content': 'Intuit Developer Program'}
        ],
        'merge_vars': [
            {
                'rcpt': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'vars': [
                    {'name': 'fname', 'content': 'John'},
                    {'name': 'account_id', 'content': 'ACC-001'}
                ]
            }
        ],
        'merge_language': 'handlebars',

        # Attachments and images
        'attachments': attachments,
        'images': images,

        # Tracking
        'track_opens': True,
        'track_clicks': True,
        'auto_text': True,
        'auto_html': False,
        'inline_css': True,

        # Tags and metadata
        'tags': ['demo', 'kitchen-sink', 'features', 'python'],
        'metadata': {
            'campaign': 'mandrill-demo',
            'version': '2.0',
            'language': 'python'
        },

        # Advanced options
        'important': True,
        'view_content_link': True,
        'preserve_recipients': False,
        'async': False
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Kitchen Sink email sent successfully!')
        print('=' * 70)

        if isinstance(result, list):
            for r in result:
                print(f"Recipient: {r['email']}")
                print(f"  Status: {r['status']}")

                if r.get('_id'):
                    print(f"  Message ID: {r['_id']}")

                if r.get('reject_reason'):
                    print(f"  Reject Reason: {r['reject_reason']}")

                print()
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 70)
        return result

    except ApiClientError as error:
        print('Error sending kitchen sink email!')
        print('=' * 70)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 70)
        return None


def send_scheduled_kitchen_sink():
    """
    Send a comprehensive email scheduled for future delivery.
    """
    # Schedule for 1 hour from now
    send_at = (datetime.utcnow() + timedelta(hours=1)
               ).strftime('%Y-%m-%d %H:%M:%S')

    message = {
        'html': '<h1>Scheduled Email</h1><p>This was scheduled in advance, {{fname}}!</p>',
        'text': 'Scheduled Email\n\nThis was scheduled in advance, {{fname}}!',
        'subject': 'Scheduled: {{subject_line}}',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': 'Scheduled Sender',
        'to': [
            {
                'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'type': 'to'
            }
        ],
        'global_merge_vars': [
            {'name': 'subject_line', 'content': 'Your Scheduled Message'}
        ],
        'merge_vars': [
            {
                'rcpt': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'vars': [
                    {'name': 'fname', 'content': 'Future Reader'}
                ]
            }
        ],
        'merge_language': 'handlebars',
        'track_opens': True,
        'track_clicks': True,
        'tags': ['scheduled', 'kitchen-sink', 'python'],
        'send_at': send_at  # Schedule for future delivery
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Email scheduled successfully!')
        print('=' * 70)
        print(f'Scheduled for: {send_at} UTC')
        print()

        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 70)
        return result

    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


def send_with_all_recipient_types():
    """
    Send email with TO, CC, and BCC recipients.
    """
    message = {
        'html': '<h1>Email with Multiple Recipient Types</h1><p>This demonstrates TO, CC, and BCC.</p>',
        'subject': 'Multiple Recipient Types Demo',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': 'Demo Sender',
        'to': [
            {'email': 'primary@example.org',
                'name': 'Primary Recipient', 'type': 'to'}
        ],
        'cc': [
            {'email': 'cc@example.org', 'name': 'CC Recipient', 'type': 'cc'}
        ],
        'bcc': [
            {'email': 'bcc@example.org', 'name': 'BCC Recipient', 'type': 'bcc'}
        ],
        'tags': ['demo', 'multiple-recipients'],
        'preserve_recipients': True  # Show all recipients in headers
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Email with multiple recipient types sent!')

        if isinstance(result, list):
            for r in result:
                print(f"  {r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')

        return result

    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('MANDRILL_API_KEY'):
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        exit(1)

    print('Sending comprehensive kitchen sink email...\n')
    send_kitchen_sink()

    # Uncomment to test scheduled sending
    # print('\n\nScheduling kitchen sink email...\n')
    # send_scheduled_kitchen_sink()

    # Uncomment to test all recipient types
    # print('\n\nSending with all recipient types...\n')
    # send_with_all_recipient_types()
