# Kitchen Sink - Example with Broad Settings (Python)

This use case demonstrates a comprehensive Mailchimp Transactional (Mandrill) message exercising many available settings in one example.

## Comprehensive Example

```python
import os
import base64
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

def read_file_as_base64(file_path):
    """Helper to read a local file and return a Base64 string."""
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def send_kitchen_sink():
    # Simple attachments
    attachments = []
    sample_pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
    if os.path.exists(sample_pdf_path):
        attachments.append({
            'type': 'application/pdf',
            'name': 'sample.pdf',
            'content': read_file_as_base64(sample_pdf_path)
        })
    
    # Inline images (empty for this demo)
    images = []
    
    # Complete Mandrill message with ALL features
    message = {
        # Basic content
        'html': '''
            <h1>Hello {{fname}}!</h1>
            <p>This email demonstrates multiple Transactional API features.</p>
            <p>Company: {{company_name}}</p>
            <p>Account: {{account_id}}</p>
            <div style="width: 50px; height: 50px; background: #007bff; border: 2px solid #0056b3; display: inline-block;"></div>
        ''',
        'text': 'Hello {{fname}}!\n\nThis email demonstrates multiple Transactional API features.\nCompany: {{company_name}}\nAccount: {{account_id}}',
        
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
            'X-Custom-Header': 'Mandrill-Demo'
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
            'version': '1.0',
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
        
        print('Kitchen Sink email sent!')
        print('=' * 50)
        
        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
                if r.get('_id'):
                    print(f"  Message ID: {r['_id']}")
                if r.get('reject_reason'):
                    print(f"  Reject Reason: {r['reject_reason']}")
        else:
            print(f'Unexpected result structure: {result}')
            
        print('=' * 50)
        
    except ApiClientError as error:
        print('Error sending kitchen sink email!')
        print('=' * 50)
        print(f'Mandrill error: {error.text}')
        print('=' * 50)

if __name__ == '__main__':
    send_kitchen_sink()
```

## Advanced Kitchen Sink with Scheduling

```python
from datetime import datetime, timedelta

def send_scheduled_kitchen_sink():
    """Send a comprehensive email scheduled for future delivery."""
    
    # Schedule for 1 hour from now
    send_at = (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    
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
        'tags': ['scheduled', 'kitchen-sink'],
        'send_at': send_at  # Schedule for future delivery
    }
    
    try:
        result = mailchimp.messages.send({'message': message})
        print(f'Email scheduled for: {send_at}')
        for r in result:
            print(f"{r['email']}: {r['status']}")
    except ApiClientError as error:
        print(f'Error: {error.text}')
```

## All Available Message Options

```python
def get_complete_message_structure():
    """
    Returns a dictionary showing all available message options.
    This is a reference - not all options are required.
    """
    return {
        # Content
        'html': '<p>HTML content</p>',
        'text': 'Plain text content',
        'subject': 'Email subject',
        
        # Sender
        'from_email': 'sender@example.org',
        'from_name': 'Sender Name',
        
        # Recipients
        'to': [
            {'email': 'recipient@example.org', 'name': 'Name', 'type': 'to'}
        ],
        
        # Headers
        'headers': {'Reply-To': 'reply@example.org'},
        
        # Merge variables
        'global_merge_vars': [{'name': 'var', 'content': 'value'}],
        'merge_vars': [{
            'rcpt': 'recipient@example.org',
            'vars': [{'name': 'var', 'content': 'value'}]
        }],
        'merge_language': 'handlebars',  # or 'mailchimp'
        
        # Attachments
        'attachments': [
            {'type': 'text/plain', 'name': 'file.txt', 'content': 'base64...'}
        ],
        'images': [
            {'type': 'image/png', 'name': 'image.png', 'content': 'base64...'}
        ],
        
        # Tracking and rendering
        'track_opens': True,
        'track_clicks': True,
        'auto_text': True,
        'auto_html': False,
        'inline_css': True,
        'url_strip_qs': False,
        'preserve_recipients': False,
        'view_content_link': True,
        
        # Delivery options
        'important': False,
        'async': False,
        'ip_pool': 'Main Pool',
        'send_at': '2024-12-31 23:59:59',  # UTC datetime string
        
        # Metadata and tagging
        'tags': ['tag1', 'tag2'],
        'subaccount': 'subaccount_id',
        'google_analytics_domains': ['example.org'],
        'google_analytics_campaign': 'campaign_name',
        'metadata': {'key': 'value'},
        'recipient_metadata': [{
            'rcpt': 'recipient@example.org',
            'values': {'key': 'value'}
        }],
        
        # Return path
        'return_path_domain': 'example.org',
        
        # Signing
        'signing_domain': 'example.org',
        
        # Tracking domain
        'tracking_domain': 'track.example.org',
        
        # Merge tag behavior
        'merge': True
    }
```

## Notes

- **Recipients**: Use `to` with `type: 'to' | 'cc' | 'bcc'` per recipient.
- **Merge**: Combine `global_merge_vars` and `merge_vars`; set `merge_language` to `handlebars` or `mailchimp`.
- **Templates**: Switch to `messages.send_template` and pass `template_name`. Use `template_content` to replace mc:edit regions (Mailchimp merge language only).
- **Attachments/Images**: Use `attachments` for files and `images` for inline CID images. Total message size max ~25MB (Base64 grows size ~33%).
- **Headers**: Add standard headers (e.g., `Reply-To`) and custom `X-` headers.
- **Tracking**: Enable `track_opens` and `track_clicks` for analytics.
- **Metadata/Tags**: Useful for analytics and grouping in the UI.
- **Scheduling**: Provide `send_at` as a UTC datetime string for future sends.
- **IP Pool**: If you use dedicated IPs, set `ip_pool` accordingly.
- **Boolean Values**: Use Python's `True`/`False` (capitalized) instead of JavaScript's `true`/`false`.
- **Method Names**: Python uses `send_template` (snake_case) instead of JavaScript's `sendTemplate` (camelCase).

## API Mapping

- Send: `messages.send()`
- Send with template: `messages.send_template()`
- All Python API methods use snake_case naming convention

