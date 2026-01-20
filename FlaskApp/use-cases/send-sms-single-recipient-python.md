# Send an SMS to a Single Recipient (Python)

This use case demonstrates how to send an SMS message to a single recipient using the Mandrill API with Python.

> **Note:** The Python SDK doesn't include the `send_sms` method yet, so we use the REST API directly with the `/api/1.1/messages/send-sms` endpoint.

## Basic Example

Here's how to send an SMS using the Mandrill REST API:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SMS_API_ENDPOINT = 'https://mandrillapp.com/api/1.1/messages/send-sms'

def send_sms(to_phone, from_phone, message_text, consent_type='onetime'):
    payload = {
        'key': os.getenv('MANDRILL_API_KEY'),
        'message': {
            'sms': {
                'text': message_text,
                'to': to_phone,           # E.164 format (e.g., +1234567890)
                'from': from_phone,       # Must be verified in Mandrill
                'consent': consent_type,
                'track_clicks': True
            }
        }
    }

    response = requests.post(
        SMS_API_ENDPOINT,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        print(f"SMS sent! Status: {result[0]['status']}")
        return result
    else:
        print(f"Failed: {response.text}")
        return None

# Send an SMS
send_sms('+1234567890', '+0987654321', 'Hello from Mandrill SMS!')
```

## API Features

| Feature | Mandrill Implementation |
|---------|-------------------------|
| **Endpoint** | `POST https://mandrillapp.com/api/1.1/messages/send-sms` |
| **Recipient** | `message.sms.to`: Phone number in E.164 format (e.g., `+1234567890`) |
| **Sender** | `message.sms.from`: Verified sender ID (E.164 number, short code, or alphanumeric) |
| **Message** | `message.sms.text`: SMS content (max 1600 characters) |
| **Consent** | `message.sms.consent`: Type of consent (`onetime`, `recurring`, `recurring-no-confirm`) |

## Message Structure

The Mandrill SMS payload requires these key properties:

- **key**: Your Mandrill API key
- **message.sms.text**: Content of the SMS message
- **message.sms.to**: Recipient's phone number in E.164 format
- **message.sms.from**: Approved sender ID (must be verified)
- **message.sms.consent**: Consent type for the message
- **message.sms.track_clicks**: Boolean to enable URL click tracking (optional)

### Phone Number Format (E.164)

Phone numbers must be in E.164 format:
- Starts with `+` followed by the country code
- No spaces, dashes, or parentheses
- Examples:
  - US: `+14155551234`
  - UK: `+442071234567`
  - Australia: `+61412345678`

### Consent Types

| Type | Description |
|------|-------------|
| `onetime` | Single transactional message (default) |
| `recurring` | Ongoing messages with confirmation |
| `recurring-no-confirm` | Ongoing messages without confirmation |

## Advanced Options

You can enhance your SMS with additional options:

```python
payload = {
    'key': api_key,
    'message': {
        'sms': {
            'text': 'Your order #12345 has shipped! Track it here: https://example.com/track/12345',
            'to': '+1234567890',
            'from': '+0987654321',
            'consent': 'onetime',
            'track_clicks': True  # Track link clicks in the message
        }
    }
}
```

## Environment Variables

Create a `.env` file in your project root with:

```
MANDRILL_API_KEY=your_api_key_here
SMS_TO_PHONE=+1234567890
SMS_FROM_PHONE=+0987654321
SMS_MESSAGE=Hello from Mandrill SMS!
SMS_CONSENT_TYPE=onetime
SMS_TRACK_CLICKS=true
```

## Error Handling

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SMS_API_ENDPOINT = 'https://mandrillapp.com/api/1.1/messages/send-sms'

def send_sms_with_error_handling(to_phone, from_phone, message_text):
    payload = {
        'key': os.getenv('MANDRILL_API_KEY'),
        'message': {
            'sms': {
                'text': message_text,
                'to': to_phone,
                'from': from_phone,
                'consent': 'onetime'
            }
        }
    }

    try:
        response = requests.post(
            SMS_API_ENDPOINT,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if result[0]['status'] == 'rejected':
                return {'success': False, 'error': f"Rejected: {result[0]['reject_reason']}"}
            return {'success': True, 'data': result}
        elif response.status_code == 401:
            return {'success': False, 'error': 'Invalid API key'}
        elif response.status_code == 400:
            return {'success': False, 'error': f"Bad request: {response.text}"}
        else:
            return {'success': False, 'error': f"HTTP {response.status_code}: {response.text}"}

    except requests.exceptions.SSLError as e:
        return {'success': False, 'error': f"SSL Error: {e}. Try setting SSL_VERIFY=false"}
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

## Prerequisites

Before sending SMS messages, ensure you have:

1. **Verified Sender Phone Number**: Your sending phone number must be verified in your Mandrill account
2. **SMS Enabled**: SMS functionality must be enabled for your account
3. **Proper Consent**: You must have appropriate consent from recipients to send SMS messages
4. **Valid API Key**: Your Mandrill API key with SMS permissions

## Common Use Cases

### Order Confirmation

```python
send_sms(
    customer_phone,
    business_phone,
    f"Your order #{order_id} has been confirmed! Expected delivery: {delivery_date}"
)
```

### Appointment Reminder

```python
send_sms(
    patient_phone,
    clinic_phone,
    f"Reminder: Your appointment is scheduled for {appointment_time}. Reply CONFIRM to confirm."
)
```

### Verification Code

```python
import random

code = random.randint(100000, 999999)
send_sms(
    user_phone,
    service_phone,
    f"Your verification code is: {code}. This code expires in 10 minutes."
)
```

### Shipping Notification

```python
send_sms(
    customer_phone,
    store_phone,
    f"Great news! Your package has shipped. Track it here: https://example.com/track/{tracking_id}"
)
```

## Notes

- **Character Limit**: SMS messages can be up to 1600 characters
- **Link Tracking**: Enable `track_clicks: True` to track link clicks in your messages
- **Rate Limits**: Be aware of SMS rate limits for your account
- **Compliance**: Ensure compliance with SMS regulations (TCPA, GDPR, etc.)
- **Costs**: SMS messages may incur additional costs depending on your plan
- **International**: International SMS delivery may have different rates and regulations

## API Response

A successful response looks like:

```json
[
  {
    "status": "sent",
    "to": "+1234567890",
    "_id": "abc123def456"
  }
]
```

Possible status values:
- `sent`: Message was sent successfully
- `queued`: Message is queued for delivery
- `rejected`: Message was rejected (check `reject_reason`)
- `invalid`: Invalid phone number or parameters

