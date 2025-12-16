# Create Template - Python

Create a reusable email template in Mandrill using Python.

## Basic Example

```python
import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

def create_template():
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
        print(f"Template created: {response['name']}")
        print(f"Template slug: {response['slug']}")
        if 'publish_name' in response:
            print(f"Published name: {response['publish_name']}")
    except ApiClientError as error:
        print(f'Error: {error.text}')

if __name__ == '__main__':
    create_template()
```

## Key Fields

- `name` - Unique template identifier
- `code` - HTML content with merge tags
- `text` - Plain text version
- `subject` - Default subject line
- `from_email`/`from_name` - Default sender
- `publish` - False = draft, True = published
- `labels` - List of labels for organization

## Advanced Template Creation

```python
def create_advanced_template():
    """Create a template with advanced features and styling."""
    
    template_data = {
        'name': 'welcome-email-v2',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'welcome@example.org'),
        'from_name': 'Welcome Team',
        'subject': 'Welcome {{fname}} - Get Started with {{company_name}}',
        'code': '''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; }
                    .header { background: #007bff; color: white; padding: 20px; }
                    .content { padding: 20px; }
                    .button { 
                        background: #28a745; 
                        color: white; 
                        padding: 10px 20px; 
                        text-decoration: none;
                        border-radius: 5px;
                        display: inline-block;
                    }
                    .footer { background: #f8f9fa; padding: 20px; text-align: center; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Welcome to {{company_name}}!</h1>
                </div>
                <div class="content">
                    <h2>Hi {{fname}} {{lname}},</h2>
                    <div mc:edit="main_content">
                        <p>We're thrilled to have you join us! Your account is now active.</p>
                        <p>Account ID: {{account_id}}</p>
                    </div>
                    <div mc:edit="cta_section">
                        <p><a href="{{dashboard_url}}" class="button">Go to Dashboard</a></p>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; {{current_year}} {{company_name}}. All rights reserved.</p>
                    <p><a href="{{unsubscribe_url}}">Unsubscribe</a></p>
                </div>
            </body>
            </html>
        ''',
        'text': '''
            Welcome to {{company_name}}!
            
            Hi {{fname}} {{lname}},
            
            We're thrilled to have you join us! Your account is now active.
            Account ID: {{account_id}}
            
            Go to your dashboard: {{dashboard_url}}
            
            © {{current_year}} {{company_name}}. All rights reserved.
            Unsubscribe: {{unsubscribe_url}}
        ''',
        'publish': False,
        'labels': ['welcome', 'onboarding', 'v2']
    }
    
    try:
        response = mailchimp.templates.add(template_data)
        print(f"Advanced template created: {response['name']}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None
```

## Template Management Functions

```python
def list_templates():
    """List all templates in your account."""
    try:
        templates = mailchimp.templates.list({'label': ''})
        print(f"Total templates: {len(templates)}")
        for template in templates:
            print(f"  - {template['name']} (slug: {template['slug']})")
    except ApiClientError as error:
        print(f'Error: {error.text}')

def get_template_info(template_name):
    """Get information about a specific template."""
    try:
        info = mailchimp.templates.info({'name': template_name})
        print(f"Template: {info['name']}")
        print(f"Subject: {info['subject']}")
        print(f"Created: {info['created_at']}")
        print(f"Updated: {info['updated_at']}")
        return info
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None

def update_template(template_name, updates):
    """Update an existing template."""
    try:
        update_data = {'name': template_name}
        update_data.update(updates)
        
        response = mailchimp.templates.update(update_data)
        print(f"Template updated: {response['name']}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None

def delete_template(template_name):
    """Delete a template."""
    try:
        response = mailchimp.templates.delete({'name': template_name})
        print(f"Template deleted: {template_name}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None
```

## Example: Create and Publish Template

```python
def create_and_publish_template():
    """Create a template and immediately publish it."""
    
    template_data = {
        'name': 'quick-notification',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'notify@example.org'),
        'from_name': 'Notification Service',
        'subject': '{{notification_type}}: {{title}}',
        'code': '''
            <h2>{{notification_type}}</h2>
            <h3>{{title}}</h3>
            <p>{{message}}</p>
            <p>Time: {{timestamp}}</p>
        ''',
        'text': '{{notification_type}}: {{title}}\n\n{{message}}\n\nTime: {{timestamp}}',
        'publish': True,  # Publish immediately
        'labels': ['notifications', 'system']
    }
    
    try:
        response = mailchimp.templates.add(template_data)
        print(f"Template created and published: {response['name']}")
        print(f"Published as: {response.get('publish_name', 'N/A')}")
        return response
    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None
```

## Template Best Practices

- **Use Descriptive Names**: Make template names clear and version them (e.g., `welcome-email-v2`)
- **Test Before Publishing**: Create as draft (`publish: False`) and test thoroughly
- **Use mc:edit Regions**: Define editable regions for flexible content updates
- **Include Plain Text**: Always provide a text version for better deliverability
- **Add Labels**: Organize templates with labels for easy management
- **Version Control**: Keep track of template versions in your naming convention
- **Responsive Design**: Use responsive HTML/CSS for mobile compatibility

## Notes

- **Template Name**: Must be unique within your account
- **mc:edit Regions**: Areas that can be customized when sending via `template_content`
- **Merge Tags**: Use Handlebars (`{{variable}}`) or Mailchimp (`*|VARIABLE|*`) syntax
- **Publishing**: Draft templates can be tested; published templates are ready for production
- **Updates**: Use `templates.update()` to modify existing templates
- **Method Names**: Python uses snake_case (`templates.add`) vs JavaScript's camelCase

