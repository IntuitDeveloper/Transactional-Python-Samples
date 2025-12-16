# Send a Single Email to a Single Recipient (Python)

This use case demonstrates how to send a single email to a single recipient using the Mandrill API with Python.

## Basic Example

Here's how to send a single email to a single recipient using the Mandrill API:

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

def send_email():
    try:
        response = mailchimp.messages.send({
            'message': message
        })
        print('Email sent successfully:')
        print(f'Full result: {response}')
        
        if response and len(response) > 0:
            print(f'Status: {response[0]["status"]}')
            print(f'Email: {response[0]["email"]}')
            print(f'Message ID: {response[0]["_id"]}')
        else:
            print(f'Unexpected result structure: {response}')
    except ApiClientError as error:
        print(f'Mandrill error: {error.text}')

if __name__ == '__main__':
    send_email()
```

## API Features

| Feature | Mandrill Implementation |
|---------|-------------------------|
| **Recipients** | `to: [{'email': 'email@example.org', 'name': 'Name', 'type': 'to'}]` |
| **Sender** | `from_email: 'email@example.org', from_name: 'Name'` |
| **Send Method** | `mailchimp.messages.send({'message': msg})` |

## Message Structure

The Mandrill message dictionary requires these key properties:

- **html**: HTML content of the email
- **text**: Plain text content (optional, but recommended)
- **subject**: Email subject line
- **from_email**: Sender's email address
- **from_name**: Sender's display name (optional)
- **to**: List of recipient dictionaries

### Recipient Dictionary Structure

Each recipient in the `to` list must be a dictionary with:

- **email**: Recipient's email address (required)
- **name**: Recipient's display name (optional)
- **type**: Recipient type - `'to'`, `'cc'`, or `'bcc'` (required)

## Advanced Options

You can enhance your email with additional options:

```python
message = {
    'html': '<p>Hello HTML world!</p>',
    'text': 'Hello plain world!',
    'subject': 'Hello world',
    'from_email': 'sender@example.org',
    'from_name': 'Sender Name',
    'to': [{
        'email': 'recipient@example.org',
        'name': 'Recipient Name',
        'type': 'to'
    }],
    'headers': {
        'Reply-To': 'replyto@example.org',
        'X-MC-Track': 'opens,clicks'
    },
    'important': True,
    'track_opens': True,
    'track_clicks': True,
    'auto_text': True,
    'auto_html': False,
    'inline_css': True,
    'tags': ['welcome', 'single-recipient'],
    'metadata': {
        'user_id': '12345',
        'campaign': 'welcome-series'
    }
}
```

## Installation

Before running this code, install the required packages:

```bash
pip install mailchimp-transactional python-dotenv
```

## Environment Variables

Create a `.env` file in your project root with:

```
MANDRILL_API_KEY=your_api_key_here
DEFAULT_FROM_EMAIL=sender@example.org
DEFAULT_FROM_NAME=Sender Name
DEFAULT_TO_EMAIL=recipient@example.org
DEFAULT_TO_NAME=Recipient Name
```

## Notes

- **Async Parameter**: Set `async: False` for immediate sending, `async: True` for background processing
- **IP Pool**: Specify `ip_pool` for dedicated IP addresses (optional)
- **Headers**: Use the `headers` dictionary for custom email headers
- **Tracking**: Enable `track_opens` and `track_clicks` for email analytics
- **Error Handling**: Use `ApiClientError` to catch Mandrill API errors

