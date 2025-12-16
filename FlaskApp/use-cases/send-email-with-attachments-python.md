# Send Email with Attachments - Python

This use case demonstrates how to attach files to emails sent via Mailchimp Transactional (Mandrill) and outlines limits and best practices.

## Basic Attachments Example

Attach one or more files by providing Base64-encoded content. The total message size (including attachments) must not exceed 25MB. Because attachments are Base64-encoded, they are roughly 33% larger than their on-disk size.

```python
import os
import base64
from datetime import datetime
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the API client
mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))

def read_file_as_base64(file_path):
    """Helper to read a local file and return a Base64 string."""
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f'Warning: File not found: {file_path}')
        return None

def send_with_attachments():
    # Prepare attachments
    attachments = []
    
    # Try to attach a PDF file if it exists
    sample_pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
    if os.path.exists(sample_pdf_path):
        pdf_content = read_file_as_base64(sample_pdf_path)
        if pdf_content:
            attachments.append({
                'type': 'application/pdf',
                'name': 'sample.pdf',
                'content': pdf_content
            })
    
    # Create a text file attachment dynamically
    text_content = (
        f'This is a demo text file created by the Mandrill Use Case.\n\n'
        f'Generated at: {datetime.now().isoformat()}\n'
    )
    attachments.append({
        'type': 'text/plain',
        'name': 'readme.txt',
        'content': base64.b64encode(text_content.encode('utf-8')).decode('utf-8')
    })
    
    message = {
        'html': '''
            <h1>Your Documents</h1>
            <p>Please find the attached files.</p>
        ''',
        'text': 'Your documents are attached.',
        'subject': 'Documents Attached',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Test Sender'),
        'to': [
            {
                'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'name': os.getenv('DEFAULT_TO_NAME', 'Test Recipient'),
                'type': 'to'
            }
        ],
        'attachments': attachments,  # List of attachments
        'tags': ['attachments', 'outbound-documents']
    }
    
    try:
        result = mailchimp.messages.send({'message': message})
        
        print('Email with attachments sent successfully!')
        print(f'Number of attachments: {len(attachments)}')
        
        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')
        
        return result
        
    except ApiClientError as error:
        print('Error sending email with attachments!')
        print(f'Mandrill API Error: {error.text}')
        return None

if __name__ == '__main__':
    send_with_attachments()
```

## Attachments Using Bytes

If you already have bytes data, convert it to Base64:

```python
def bytes_to_base64(data):
    """Convert bytes to Base64 string."""
    return base64.b64encode(data).decode('utf-8')

def send_bytes_as_attachment(data, filename, mime_type):
    """Send bytes data as an email attachment."""
    message = {
        'html': '<p>Attached file from bytes.</p>',
        'text': 'Attached file from bytes.',
        'subject': 'Bytes Attachment',
        'from_email': 'attachments@example.org',
        'from_name': 'Attachment Service',
        'to': [{'email': 'john@example.org', 'type': 'to'}],
        'attachments': [
            {
                'type': mime_type or 'application/octet-stream',
                'name': filename or 'file.bin',
                'content': bytes_to_base64(data)
            }
        ]
    }
    
    try:
        result = mailchimp.messages.send({'message': message})
        
        if isinstance(result, list) and len(result) > 0:
            print(f'Attachment sent: {result[0]["status"]}')
        else:
            print(f'Unexpected result structure: {result}')
    except ApiClientError as error:
        print(f'Error: {error.text}')
```

## Working with Different File Types

```python
def send_multiple_file_types():
    """Example showing different file types as attachments."""
    
    attachments = []
    
    # PDF file
    if os.path.exists('document.pdf'):
        attachments.append({
            'type': 'application/pdf',
            'name': 'document.pdf',
            'content': read_file_as_base64('document.pdf')
        })
    
    # Image file
    if os.path.exists('chart.png'):
        attachments.append({
            'type': 'image/png',
            'name': 'chart.png',
            'content': read_file_as_base64('chart.png')
        })
    
    # CSV file
    csv_content = "Name,Email,Status\nJohn,john@example.org,Active\n"
    attachments.append({
        'type': 'text/csv',
        'name': 'report.csv',
        'content': base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    })
    
    # JSON file
    import json
    json_data = {'status': 'success', 'count': 42}
    attachments.append({
        'type': 'application/json',
        'name': 'data.json',
        'content': base64.b64encode(
            json.dumps(json_data, indent=2).encode('utf-8')
        ).decode('utf-8')
    })
    
    message = {
        'html': '<h1>Multiple File Types</h1><p>Various file formats attached.</p>',
        'subject': 'Multiple Attachments',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'to': [{'email': os.getenv('DEFAULT_TO_EMAIL', 'test@example.org'), 'type': 'to'}],
        'attachments': attachments
    }
    
    try:
        result = mailchimp.messages.send({'message': message})
        
        if isinstance(result, list):
            print(f'Email with {len(attachments)} attachments sent successfully')
            for r in result:
                print(f"  {r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')
    except ApiClientError as error:
        print(f'Error: {error.text}')
```

## Limits and Processing

- **Total Message Size**: Up to 25MB (includes the message body + attachments + headers).
- **Base64 Overhead**: Attachments are Base64-encoded, increasing size by ~33%. A 15MB file on disk becomes ~20MB over the wire.
- **Virus Scanning**: All attachments are scanned by multiple engines to help ensure safety for recipients.
- **No Per-File Limit**: There is no specific limit for individual attachments beyond the total message size.

## Best Practices

- **Keep Attachments Small**: Prefer < 10MB combined to ensure deliverability and reduce scan time.
- **Use Accurate MIME Types**: Set the `type` field properly (e.g., `application/pdf`, `image/png`).
- **Validate Sizes**: Pre-check content size and account for Base64 growth before sending.
- **Fallback Links**: For large or multiple files, consider hosting and linking instead of emailing.
- **Security**: Only attach files from trusted sources; scan files before sending.
- **Tracking**: Add tags and metadata for downstream analytics.

## Common MIME Types

```python
MIME_TYPES = {
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.txt': 'text/plain',
    '.csv': 'text/csv',
    '.json': 'application/json',
    '.zip': 'application/zip'
}
```

## Notes

- **Attachments Field**: Provide a list of dictionaries `{'type': ..., 'name': ..., 'content': ...}` where `content` is Base64.
- **Inline Images**: Use the `images` list for content intended to render inside the email body (see inline images use case).
- **Delivery Timing**: Large attachments can add processing time due to scanning.
- **Error Handling**: Handle `ApiClientError` for malformed attachments and runtime errors for oversize messages.

