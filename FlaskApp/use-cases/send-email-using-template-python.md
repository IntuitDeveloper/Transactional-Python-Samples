# Send Email Using Stored Template - Python

Send an email using a stored template with `messages.send_template`. Provide the template name, optional `template_content` (for mc:edit regions), and a standard `message` with recipients and merge data.

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

def send_with_template():
    template_name = 'hello-template'
    
    message = {
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'subject': 'Welcome, {{fname}}',  # Can be overridden even if template has a default
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
    
    # Replace mc:edit regions in template (works with both Handlebars and Mailchimp)
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
        
        print('Template-based emails sent:')
        if isinstance(result, list):
            for r in result:
                print(f"   {r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')
    except ApiClientError as error:
        print(f'Mandrill error: {error.text}')

if __name__ == '__main__':
    send_with_template()
```

## Advanced Template Usage

```python
def send_template_with_multiple_recipients():
    """Send template-based email to multiple recipients with personalized content."""
    
    template_name = 'welcome-template'
    
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
            'name': 'main_content',
            'content': '<p>Your personalized welcome message goes here.</p>'
        }
    ]
    
    try:
        result = mailchimp.messages.send_template({
            'template_name': template_name,
            'template_content': template_content,
            'message': message
        })
        
        print('Batch template emails sent:')
        for r in result:
            print(f"   {r['email']}: {r['status']}")
            
    except ApiClientError as error:
        print(f'Error: {error.text}')
```

## Notes

- **Template name**: Use the template's `name`/slug as shown in the Templates UI or API.
- **Merge language**: Choose `handlebars` or `mailchimp` via `merge_language` per message.
- **Editable regions**: Use `template_content` to replace `mc:edit` regions (only with Mailchimp merge language templates).
- **Overrides**: `subject`, `from_email`, and `from_name` can be overridden at send-time.
- **Method Name**: In Python, use `send_template` (snake_case) instead of JavaScript's `sendTemplate` (camelCase).

## API Mapping

- Send with template: `messages.send_template()`
- Python uses snake_case for method names (vs JavaScript's camelCase)

