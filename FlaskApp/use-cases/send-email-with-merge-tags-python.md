# Send Email with Merge Tags (Dynamic Content) - Python

This use case demonstrates how to personalize emails using merge tags for dynamic content like names, order information, and custom data.

## Basic Merge Tags Example

Use merge tags to personalize content for each recipient:

```python
import os
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

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
            'content': 'Premium'  # Default value
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

def send_personalized_email():
    try:
        result = mailchimp.messages.send({'message': message})
        print('Personalized emails sent:')
        
        if isinstance(result, list):
            for recipient in result:
                print(f"{recipient['email']}: {recipient['status']}")
        else:
            print(f'Unexpected result structure: {result}')
    except ApiClientError as error:
        print(f'Mandrill error: {error.text}')

if __name__ == '__main__':
    send_personalized_email()
```

## Merge Language Options

| Language | Syntax | Example | Use Case |
|---|---|---|---|
| handlebars | {{variable}} | Hello {{name}}! | Complex logic, loops, conditionals |
| mailchimp | `*|VARIABLE|*` | Hello *|NAME|*! | Simple substitutions, legacy compatibility |

## Key Features

| Feature | Description | Example |
|---|---|---|
| Global Merge Vars | Apply to all recipients | Company name, promotion details |
| Recipient Merge Vars | Specific to each recipient | Personal names, order details |
| Merge Language | Choose syntax style | handlebars or mailchimp |
| Complex Data | Dictionaries and lists | Order items, address objects |
| Fallback Values | Default when data missing | {{name 'Customer'}} |

## Multiple Recipients Example

```python
def send_to_multiple_recipients():
    message = {
        'html': '<h1>Welcome {{fname}}!</h1><p>Your account {{account_id}} is active.</p>',
        'subject': 'Welcome {{fname}}!',
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
        'merge_vars': [
            {
                'rcpt': 'john@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'John'},
                    {'name': 'account_id', 'content': 'ACC-001'}
                ]
            },
            {
                'rcpt': 'jane@example.org',
                'vars': [
                    {'name': 'fname', 'content': 'Jane'},
                    {'name': 'account_id', 'content': 'ACC-002'}
                ]
            }
        ],
        'merge_language': 'handlebars'
    }
    
    try:
        result = mailchimp.messages.send({'message': message})
        for recipient in result:
            print(f"{recipient['email']}: {recipient['status']}")
    except ApiClientError as error:
        print(f'Error: {error.text}')
```

## Notes

- **Merge Tag Format**: Use alphanumeric characters and underscores only (no colons)
- **Content Length**: Generally unlimited for API usage
- **Global vs Recipient**: Global vars apply to all; recipient vars are specific to each email
- **Language Setting**: Can be set globally in account or per-message via `merge_language`
- **Handlebars Benefits**: Supports loops, conditionals, and complex logic
- **Template Conversion**: Mailchimp templates auto-convert to Handlebars when imported
- **Error Handling**: Always handle cases where merge data might be missing

