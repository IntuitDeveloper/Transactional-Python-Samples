"""
Send Email Using Stored Template with Mandrill API

This script demonstrates how to send emails using pre-created templates
with merge tags and dynamic content.

Usage:
    python email_with_template.py

Requirements:
    - mailchimp-transactional
    - python-dotenv

Note: Templates will be automatically created if they don't exist.
"""

import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Template definitions matching the Mandrill account
TEMPLATES = {
    'template1': {
        'name': 'template1',
        'subject': 'Hello {{fname}}!',
        'code': '''<h1>Hello {{fname}}!</h1>
                <div mc:edit="welcome_message">
                  <p>Welcome to {{company_name}}.</p>
                </div>
                <p>Your account: {{account_id}}</p>''',
        'text': 'This is a simple greetings from template1.',
        'labels': ['demo', 'hello'],
        'mc_edit_region': 'welcome_message'
    },
    'template2': {
        'name': 'template2',
        'subject': 'Greetings {{fname}}!',
        'code': '''<h1>Greetings {{fname}}!</h1>
                <p>Hope your Account: {{account_id}} is all set in Company: {{company_name}}</p>
                <div mc:edit="goodbye_message">
                  <p>We will see you soon {{company_name}}.</p>
                </div>''',
        'text': 'This is a simple greetings from template2.',
        'labels': ['demo', 'hello'],
        'mc_edit_region': 'goodbye_message'
    }
}


def get_mailchimp_client():
    """
    Get a Mailchimp Transactional client.
    Creates a new client each time to ensure correct API key is used.
    """
    api_key = os.getenv('MANDRILL_API_KEY')
    if not api_key:
        raise ValueError("MANDRILL_API_KEY not found in environment variables")
    return MailchimpTransactional.Client(api_key)


def template_exists(template_name):
    """
    Check if a template exists in Mandrill.
    """
    try:
        client = get_mailchimp_client()
        templates = client.templates.list({'label': ''})
        return any(t['name'] == template_name for t in templates)
    except ApiClientError:
        return False


def ensure_template_exists(template_name):
    """
    Ensure a template exists, creating it if necessary.
    Returns True if template exists or was created successfully.
    """
    if template_exists(template_name):
        print(f'Template "{template_name}" already exists.')
        return True
    
    if template_name not in TEMPLATES:
        print(f'Unknown template: {template_name}')
        return False
    
    template_def = TEMPLATES[template_name]
    
    template_data = {
        'name': template_def['name'],
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'subject': template_def['subject'],
        'code': template_def['code'],
        'text': template_def['text'],
        'publish': False,
        'labels': template_def['labels']
    }
    
    try:
        client = get_mailchimp_client()
        response = client.templates.add(template_data)
        print(f'Template "{template_name}" created successfully!')
        return True
    except ApiClientError as error:
        print(f'Error creating template: {error.text}')
        return False


def send_with_template(template_name='template1'):
    """
    Send an email using a stored template.
    Creates the template first if it doesn't exist.
    """
    # Ensure template exists before sending
    if not ensure_template_exists(template_name):
        print(f'Failed to ensure template "{template_name}" exists.')
        return None

    template_def = TEMPLATES.get(template_name, TEMPLATES['template1'])

    message = {
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'subject': 'Welcome, {{fname}}',
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

    # Template content for mc:edit regions
    if template_name == 'template1':
        template_content = [
            {
                'name': 'welcome_message',
                'content': "<p>Thanks for joining <strong>{{company_name}}</strong>! We're excited to have you on board.</p>"
            }
        ]
    else:
        template_content = [
            {
                'name': 'goodbye_message',
                'content': "<p>We don't have much updates, but this email is for your account: {{account_id}} in company: {{company_name}}</p>"
            }
        ]

    try:
        client = get_mailchimp_client()
        result = client.messages.send_template({
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
        return None


def send_template_to_multiple_recipients(template_name='template1'):
    """
    Send a template-based email to multiple recipients with personalized data.
    """
    # Ensure template exists before sending
    if not ensure_template_exists(template_name):
        print(f'Failed to ensure template "{template_name}" exists.')
        return None

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
        client = get_mailchimp_client()
        result = client.messages.send_template({
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

    # Use SELECTED_TEMPLATE from environment or default to template1
    template_name = os.getenv('SELECTED_TEMPLATE', 'template1')

    print(f'Sending email with template: {template_name}...\n')
    send_with_template(template_name)

    # Uncomment to test multiple recipients
    # print('\n\nSending template to multiple recipients...\n')
    # send_template_to_multiple_recipients(template_name)
