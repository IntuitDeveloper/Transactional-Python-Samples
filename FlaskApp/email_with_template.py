"""
Send Email Using Stored Template with Mandrill API

This script demonstrates how to send emails using pre-created templates
with merge tags and dynamic content.

Usage:
    python email_with_template.py

Requirements:
    - mailchimp-transactional
    - python-dotenv

Note: You must first create a template using create_template.py or via the Mandrill UI.
"""

import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))


def send_with_template():
    """
    Send an email using a stored template.
    """
    template_name = 'hello-template'

    message = {
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'subject': 'Welcome, {{fname}}',  # Can override template default
        'to': [
            {
                'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
                'type': 'to'
            }
        ],
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
        'tags': ['onboarding', 'welcome']
    }

    # Replace mc:edit regions in template
    template_content = [
        {
            'name': 'welcome_message',
            'content': '<p>Thanks for joining <strong>{{company_name}}</strong>! We\'re excited to have you on board.</p>'
        }
    ]

    try:
        result = mailchimp.messages.send_template({
            'template_name': template_name,
            'template_content': template_content,
            'message': message
        })

        print('Template-based email sent successfully!')
        print('=' * 50)

        if isinstance(result, list):
            for r in result:
                print(f"   {r['email']}: {r['status']}")
                if r.get('_id'):
                    print(f"      Message ID: {r['_id']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
        return result

    except ApiClientError as error:
        print('Error sending template-based email!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)

        if 'Unknown_Template' in str(error.text):
            print(f'\nTemplate "{template_name}" does not exist.')
            print('Please create it first using create_template.py')

        return None


def send_template_to_multiple_recipients():
    """
    Send a template-based email to multiple recipients with personalized data.
    """
    template_name = 'hello-template'

    message = {
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': 'Welcome Team',
        'subject': 'Welcome {{fname}} to {{company_name}}',
        'to': [
            {'email': 'user1@example.org', 'name': 'User One', 'type': 'to'},
            {'email': 'user2@example.org', 'name': 'User Two', 'type': 'to'}
        ],
        'global_merge_vars': [
            {'name': 'company_name', 'content': 'Intuit Developer Program'}
        ],
        'merge_vars': [
            {
                'rcpt': 'user1@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'Alice'},
                    {'name': 'account_id', 'content': 'ACC-101'}
                ]
            },
            {
                'rcpt': 'user2@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'Bob'},
                    {'name': 'account_id', 'content': 'ACC-102'}
                ]
            }
        ],
        'merge_language': 'handlebars',
        'track_opens': True,
        'track_clicks': True,
        'tags': ['welcome', 'batch-send']
    }

    template_content = [
        {
            'name': 'welcome_message',
            'content': '<p>Your personalized welcome message!</p>'
        }
    ]

    try:
        result = mailchimp.messages.send_template({
            'template_name': template_name,
            'template_content': template_content,
            'message': message
        })

        print('Batch template emails sent!')
        print('=' * 50)

        if isinstance(result, list):
            for r in result:
                print(f"   {r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
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

    print('Sending email with template...\n')
    send_with_template()

    # Uncomment to test multiple recipients
    # print('\n\nSending template to multiple recipients...\n')
    # send_template_to_multiple_recipients()
