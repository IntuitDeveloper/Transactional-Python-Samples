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

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

def create_template():
    """
    Create a basic email template.
    """
    template_data = {
        'name': 'hello-template',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'subject': 'Hello {{fname}}!',
        'code': '''
            <h1>Hello {{fname}}!</h1>
            <div mc:edit="welcome_message">
                <p>Welcome to {{company_name}}.</p>
            </div>
            <p>Your account: {{account_id}}</p>
        ''',
        'text': 'Hello {{fname}}!\n\nWelcome to {{company_name}}.\nYour account: {{account_id}}',
        'publish': False,
        'labels': ['hello', 'demo']
    }
    
    try:
        response = mailchimp.templates.add(template_data)
        
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
        return response
        
    except ApiClientError as error:
        print('Error creating template!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        
        if 'A template with that name already exists' in str(error.text):
            print('\nA template with this name already exists.')
            print('Try using a different name or delete the existing template.')
        
        print('=' * 50)
        return None

def create_advanced_template():
    """
    Create a template with advanced features and styling.
    """
    template_data = {
        'name': 'welcome-email-advanced',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'welcome@example.org'),
        'from_name': 'Welcome Team',
        'subject': 'Welcome {{fname}} - Get Started with {{company_name}}',
        'code': '''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }
                    .header { background: #007bff; color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; }
                    .button { 
                        background: #28a745; 
                        color: white; 
                        padding: 12px 24px; 
                        text-decoration: none;
                        border-radius: 5px;
                        display: inline-block;
                        margin: 10px 0;
                    }
                    .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Welcome to {{company_name}}!</h1>
                </div>
                <div class="content">
                    <h2>Hi {{fname}} {{lname}},</h2>
                    <div mc:edit="main_content">
                        <p>We're thrilled to have you join us! Your account is now active and ready to use.</p>
                        <p>Account ID: <strong>{{account_id}}</strong></p>
                    </div>
                    <div mc:edit="cta_section">
                        <p><a href="{{dashboard_url}}" class="button">Go to Dashboard</a></p>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; {{current_year}} {{company_name}}. All rights reserved.</p>
                    <p><a href="{{unsubscribe_url}}" style="color: #666;">Unsubscribe</a></p>
                </div>
            </body>
            </html>
        ''',
        'text': '''
            Welcome to {{company_name}}!
            
            Hi {{fname}} {{lname}},
            
            We're thrilled to have you join us! Your account is now active and ready to use.
            Account ID: {{account_id}}
            
            Go to your dashboard: {{dashboard_url}}
            
            © {{current_year}} {{company_name}}. All rights reserved.
            Unsubscribe: {{unsubscribe_url}}
        ''',
        'publish': False,
        'labels': ['welcome', 'onboarding', 'advanced']
    }
    
    try:
        response = mailchimp.templates.add(template_data)
        print(f"Advanced template created: {response['name']}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None

def list_templates():
    """
    List all templates in your account.
    """
    try:
        templates = mailchimp.templates.list({'label': ''})
        
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
        info = mailchimp.templates.info({'name': template_name})
        
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
        response = mailchimp.templates.delete({'name': template_name})
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
    
    print('Creating email template...\n')
    create_template()
    
    print('\n\nListing all templates...\n')
    list_templates()
    
    # Uncomment to create an advanced template
    # print('\n\nCreating advanced template...\n')
    # create_advanced_template()
    
    # Uncomment to get info about a specific template
    # print('\n\nGetting template info...\n')
    # get_template_info('hello-template')
    
    # Uncomment to delete a template (use with caution!)
    # print('\n\nDeleting template...\n')
    # delete_template('hello-template')

