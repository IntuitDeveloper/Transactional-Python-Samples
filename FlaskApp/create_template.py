"""
Create Email Template using Mandrill API

This script demonstrates how to create reusable email templates
in Mandrill that can be used with messages.send_template().

Usage:
    python create_template.py

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


def get_mailchimp_client():
    """
    Get a Mailchimp Transactional client.
    """
    api_key = os.getenv('MANDRILL_API_KEY')
    if not api_key:
        raise ValueError("MANDRILL_API_KEY not found in environment variables")
    return MailchimpTransactional.Client(api_key)


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
        'labels': ['demo', 'hello']
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
        'labels': ['demo', 'hello']
    }
}


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


def create_template(template_name):
    """
    Create a template if it doesn't already exist.
    """
    if template_exists(template_name):
        print(f'Template "{template_name}" already exists.')
        return {'success': True, 'exists': True}
    
    if template_name not in TEMPLATES:
        print(f'Unknown template: {template_name}')
        return {'success': False, 'error': f'Unknown template: {template_name}'}
    
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
        
        print('Template created successfully!')
        print('=' * 50)
        print(f"Name: {response['name']}")
        print(f"Slug: {response['slug']}")
        print(f"Created at: {response.get('created_at', 'N/A')}")
        
        if response.get('publish_name'):
            print(f"Published as: {response['publish_name']}")
        else:
            print('Status: Draft (not published)')
        
        print('=' * 50)
        return {'success': True, 'exists': False, 'result': response}
        
    except ApiClientError as error:
        print('Error creating template!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)
        return {'success': False, 'error': error.text}


def ensure_template_exists(template_name):
    """
    Ensure a template exists, creating it if necessary.
    Returns True if template exists or was created successfully.
    """
    result = create_template(template_name)
    return result['success']


def list_templates():
    """
    List all templates in your account.
    """
    try:
        client = get_mailchimp_client()
        templates = client.templates.list({'label': ''})
        
        print('Your Mandrill Templates:')
        print('=' * 50)
        print(f"Total templates: {len(templates)}")
        print()
        
        for template in templates:
            print(f"  • {template['name']}")
            print(f"    Slug: {template['slug']}")
            if template.get('labels'):
                print(f"    Labels: {', '.join(template['labels'])}")
            print()
        
        print('=' * 50)
        return templates
        
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


def get_template_info(template_name):
    """
    Get detailed information about a specific template.
    """
    try:
        client = get_mailchimp_client()
        info = client.templates.info({'name': template_name})
        
        print(f'Template Information:')
        print('=' * 50)
        print(f"Name: {info['name']}")
        print(f"Subject: {info['subject']}")
        print(f"From: {info['from_name']} <{info['from_email']}>")
        print(f"Created: {info.get('created_at', 'N/A')}")
        print(f"Updated: {info.get('updated_at', 'N/A')}")
        
        if info.get('labels'):
            print(f"Labels: {', '.join(info['labels'])}")
        
        print('=' * 50)
        return info
        
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


def delete_template(template_name):
    """
    Delete a template (use with caution).
    """
    try:
        client = get_mailchimp_client()
        response = client.templates.delete({'name': template_name})
        print(f"Template deleted: {template_name}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('MANDRILL_API_KEY'):
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        exit(1)
    
    print('Creating email templates...\n')
    
    # Create template1
    print('Creating template1...')
    create_template('template1')
    
    # Create template2
    print('\nCreating template2...')
    create_template('template2')
    
    print('\n\nListing all templates...\n')
    list_templates()
