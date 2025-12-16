# Python Scripts for Mandrill API Use Cases

This directory contains Python implementations of Mandrill API use cases using the `mailchimp_transactional` library.

## Prerequisites

- Python 3.7 or higher
- A Mandrill API key from [Mailchimp](https://mandrillapp.com/)

## Installation

1. Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

Or install packages individually:

```bash
pip3 install mailchimp-transactional python-dotenv
```

## Configuration

1. Copy the `.env.example` file to `.env` in the scripts directory:

```bash
cp env.example .env
```

2. Edit the `.env` file and add your credentials:

```
MANDRILL_API_KEY=your_mandrill_api_key_here
DEFAULT_FROM_EMAIL=sender@yourdomain.com
DEFAULT_FROM_NAME=Your Name
DEFAULT_TO_EMAIL=recipient@example.com
DEFAULT_TO_NAME=Recipient Name
```

## Available Python Scripts

### 1. Send Single Email to Single Recipient

**File:** `email_with_single_recipient.py`

Demonstrates how to send a basic email to a single recipient.

```bash
python email_with_single_recipient.py
```

**Features:**
- Basic email sending
- HTML and plain text content
- Custom headers
- Advanced options with tracking and metadata

### 2. Send Email with Merge Tags

**File:** `email_with_merge_tags.py`

Personalize emails using merge tags for dynamic content.

```bash
python email_with_merge_tags.py
```

**Features:**
- Global merge variables (apply to all recipients)
- Recipient-specific merge variables
- Handlebars template syntax
- Multiple recipient personalization

### 3. Send Email Using Template

**File:** `email_with_template.py`

Send emails using pre-created Mandrill templates.

```bash
python email_with_template.py
```

**Features:**
- Use stored templates
- Override template defaults
- Dynamic content with merge tags
- mc:edit region replacement

**Note:** You must first create a template using `create_template.py` or via the Mandrill UI.

### 4. Send Email with Attachments

**File:** `email_with_attachments.py`

Attach files (PDF, CSV, JSON, etc.) to your emails.

```bash
python email_with_attachments.py
```

**Features:**
- Attach local files (PDF, images, etc.)
- Create dynamic attachments (CSV, JSON, text)
- Base64 encoding handling
- Multiple attachment types

### 5. Create Template

**File:** `create_template.py`

Create and manage reusable email templates.

```bash
python create_template.py
```

**Features:**
- Create new templates (if not already available)
- List all templates
- Get template information
- Update and delete templates
- mc:edit regions for dynamic content

### 6. Kitchen Sink - All Features

**File:** `kitchen_sink_email.py`

Comprehensive example demonstrating all Mandrill features.

```bash
python kitchen_sink_email.py
```

**Features:**
- All message options in one example
- Attachments, tracking, metadata
- Multiple recipient types (TO, CC, BCC)
- Scheduled sending
- Advanced headers and custom fields

## Script Structure

Each Python script follows this structure:

1. **Import statements** - Required libraries
2. **Environment configuration** - Load API credentials
3. **Function definitions** - Reusable email sending functions
4. **Main execution block** - Run the example

## Error Handling

All scripts include error handling for:
- Missing API credentials
- API client errors
- Network issues
- Invalid email addresses

Example error handling pattern:

```python
try:
    response = mailchimp.messages.send({'message': message})
    # Handle success
except ApiClientError as error:
    print(f'Mandrill API Error: {error.text}')
```

## API Response

A successful API response includes:

```python
[
    {
        "email": "recipient@example.org",
        "status": "sent",  # or "queued", "rejected", "invalid"
        "_id": "abc123",
        "reject_reason": None  # or reason if rejected
    }
]
```

## Common Status Values

- `sent` - Message was successfully sent
- `queued` - Message is queued for sending
- `scheduled` - Message is scheduled for future sending
- `rejected` - Message was rejected
- `invalid` - Invalid recipient email address

## Testing

To test without sending real emails, you can use Mandrill's test mode or verify your code with print statements before actual sending.

## Resources

- [Mandrill API Documentation](https://mailchimp.com/developer/transactional/api/)
- [Python SDK on GitHub](https://github.com/mailchimp/mailchimp-transactional-python)
- [API Status Codes](https://mailchimp.com/developer/transactional/api/messages/send-new-message/)

## Support

For issues with:
- **Mandrill API**: Contact Mailchimp support
- **Python SDK**: Open an issue on the GitHub repository
- **These examples**: Check the use-cases documentation

## License

See the LICENSE file in the root directory.

