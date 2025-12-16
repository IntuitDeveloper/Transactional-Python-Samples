"""
Send Email with Merge Tags using Mandrill API

This script demonstrates how to personalize emails using merge tags
for dynamic content like names, order information, and custom data.

Usage:
    python email_with_merge_tags.py

Requirements:
    - mailchimp-transactional
    - python-dotenv
"""

import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))


def send_personalized_email():
    """
    Send a personalized email using merge tags for dynamic content.
    """
    message = {
        'html': '''
            <h1>Welcome {{fname}}!</h1>
            <p>Hi {{fname}} {{lname}},</p>
            <p>Thanks for joining the {{company_name}}! Your account is now active.</p>
            <p>Your membership level: {{membership_level}}</p>
            <p>Best regards,<br>The {{company_name}} Team</p>
        ''',
        'text': '''
            Welcome {{fname}}!
            
            Hi {{fname}} {{lname}},
            
            Thanks for joining the {{company_name}}! Your account is now active.
            Your membership level: {{membership_level}}
            
            Best regards,
            The {{company_name}} Team
        ''',
        'subject': 'Welcome to {{company_name}}, {{fname}}!',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'to': [{
            'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
            'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
            'type': 'to'
        }],
        'headers': {
            'Reply-To': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org')
        },
        # Global merge variables (apply to all recipients)
        'global_merge_vars': [
            {
                'name': 'company_name',
                'content': 'Intuit Developer Program'
            },
            {
                'name': 'membership_level',
                'content': 'Premium'
            }
        ],
        # Recipient-specific merge variables
        'merge_vars': [
            {
                'rcpt': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'vars': [
                    {
                        'name': 'fname',
                        'content': 'John'
                    },
                    {
                        'name': 'lname',
                        'content': 'Smith'
                    }
                ]
            }
        ],
        'merge_language': 'handlebars'  # or 'mailchimp'
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Personalized email sent successfully!')
        print('=' * 50)

        if isinstance(result, list):
            for recipient in result:
                print(f"{recipient['email']}: {recipient['status']}")
                if recipient.get('_id'):
                    print(f"  Message ID: {recipient['_id']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
        return result

    except ApiClientError as error:
        print('Error sending personalized email!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)
        return None


def send_to_multiple_recipients():
    """
    Send personalized emails to multiple recipients with different merge data.
    """
    message = {
        'html': '''
            <h1>Welcome {{fname}}!</h1>
            <p>Your account {{account_id}} is now active.</p>
            <p>Membership: {{membership_level}}</p>
        ''',
        'subject': 'Welcome {{fname}} to {{company_name}}!',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'to': [
            {
                'email': 'john@example.org',
                'name': 'John Smith',
                'type': 'to'
            },
            {
                'email': 'jane@example.org',
                'name': 'Jane Doe',
                'type': 'to'
            }
        ],
        'global_merge_vars': [
            {'name': 'company_name', 'content': 'Intuit Developer Program'}
        ],
        'merge_vars': [
            {
                'rcpt': 'john@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'John'},
                    {'name': 'account_id', 'content': 'ACC-001'},
                    {'name': 'membership_level', 'content': 'Premium'}
                ]
            },
            {
                'rcpt': 'jane@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'Jane'},
                    {'name': 'account_id', 'content': 'ACC-002'},
                    {'name': 'membership_level', 'content': 'Standard'}
                ]
            }
        ],
        'merge_language': 'handlebars'
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Batch personalized emails sent!')
        print('=' * 50)

        if isinstance(result, list):
            for recipient in result:
                print(f"{recipient['email']}: {recipient['status']}")
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

    print('Sending personalized email...\n')
    send_personalized_email()

    # Uncomment to test multiple recipients
    # print('\n\nSending to multiple recipients...\n')
    # send_to_multiple_recipients()
