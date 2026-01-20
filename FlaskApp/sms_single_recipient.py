#!/usr/bin/env python3
"""
Send an SMS to a Single Recipient using Mandrill API

This script demonstrates how to send an SMS message to a single recipient
using the Mailchimp Transactional (Mandrill) API.

Usage:
    python sms_single_recipient.py

Requirements:
    - requests
    - python-dotenv

Install with:
    pip install requests python-dotenv
    
Or with requirements.txt:
    pip install -r requirements.txt

Note: SMS functionality uses the Mandrill REST API v1.1 directly since the
Python SDK doesn't include the send_sms method yet.
"""

import os
import json
import requests
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SMS API endpoint (note: uses API version 1.1, not 1.0)
SMS_API_ENDPOINT = 'https://mandrillapp.com/api/1.1/messages/send-sms'

# SSL verification mode - set SSL_VERIFY=false if behind corporate proxy
SSL_VERIFY = os.getenv('SSL_VERIFY', 'true').lower() != 'false'


def send_sms(to=None, from_phone=None, text=None, consent=None, track_clicks=None):
    """
    Send an SMS message using the Mandrill API.
    
    Args:
        to (str): Recipient phone number in E.164 format (e.g., +1234567890)
        from_phone (str): Sender phone number (must be verified in Mandrill)
        text (str): SMS message content (max 1600 characters)
        consent (str): Consent type ('onetime', 'recurring', 'recurring-no-confirm')
        track_clicks (bool): Whether to track link clicks in the message
    
    Returns:
        dict or None: API response on success, None on failure
    """
    api_key = os.getenv('MANDRILL_API_KEY')
    
    if not api_key:
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        return None
    
    # Build the SMS message payload with defaults from environment
    to_phone = to or os.getenv('SMS_TO_PHONE', '+1234567890')
    sender_phone = from_phone or os.getenv('SMS_FROM_PHONE', '+0987654321')
    message_text = text or os.getenv('SMS_MESSAGE', 'Hello from Mandrill SMS! This is a test message.')
    consent_type = consent or os.getenv('SMS_CONSENT_TYPE', 'onetime')
    should_track_clicks = track_clicks if track_clicks is not None else os.getenv('SMS_TRACK_CLICKS', 'false').lower() == 'true'
    
    payload = {
        'key': api_key,
        'message': {
            'sms': {
                'text': message_text,
                'to': to_phone,
                'from': sender_phone,
                'consent': consent_type,
                'track_clicks': should_track_clicks
            }
        }
    }
    
    try:
        # Set up the request
        headers = {'Content-Type': 'application/json'}
        
        if not SSL_VERIFY:
            print("⚠️  SSL verification disabled (SSL_VERIFY=false)")
        
        # Send the request
        response = requests.post(
            SMS_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30,
            verify=SSL_VERIFY
        )
        
        print('SMS Request sent!')
        print('=' * 50)
        
        if response.status_code == 200:
            result = response.json()
            print('SMS sent successfully!')
            print(f'Response: {json.dumps(result, indent=2)}')
            
            # Display key details from the response
            if isinstance(result, list) and len(result) > 0:
                first_result = result[0]
                print('\nDetails:')
                if first_result.get('status'):
                    print(f"  Status: {first_result['status']}")
                if first_result.get('to'):
                    print(f"  To: {first_result['to']}")
                if first_result.get('_id'):
                    print(f"  Message ID: {first_result['_id']}")
                if first_result.get('reject_reason'):
                    print(f"  Reject Reason: {first_result['reject_reason']}")
            elif isinstance(result, dict):
                if result.get('status'):
                    print(f"  Status: {result['status']}")
                if result.get('_id'):
                    print(f"  Message ID: {result['_id']}")
            
            print('=' * 50)
            return result
        else:
            try:
                error_body = response.json()
            except:
                error_body = response.text
            
            print('SMS sending failed!')
            print(f'HTTP Status: {response.status_code}')
            if isinstance(error_body, dict):
                print(f'Error: {json.dumps(error_body, indent=2)}')
            else:
                print(f'Error: {error_body}')
            print('=' * 50)
            return None
            
    except requests.exceptions.SSLError as e:
        print('SSL Certificate Error!')
        print('=' * 50)
        print(f'Error: {e}')
        print('')
        print("💡 TIP: If you're behind a corporate proxy, add this to your .env file:")
        print("   SSL_VERIFY=false")
        print('=' * 50)
        return None
    except requests.exceptions.Timeout:
        print('Request Timeout!')
        print('=' * 50)
        print('The request timed out after 30 seconds.')
        print('=' * 50)
        return None
    except Exception as e:
        print('Error sending SMS!')
        print('=' * 50)
        print(f'Error: {e}')
        print('=' * 50)
        return None


def send_sms_with_error_handling(to_phone, from_phone, message_text, consent_type='onetime'):
    """
    Send an SMS with comprehensive error handling.
    
    Args:
        to_phone (str): Recipient phone number in E.164 format
        from_phone (str): Sender phone number
        message_text (str): SMS message content
        consent_type (str): Type of consent
    
    Returns:
        dict: Result with 'success' boolean and 'data' or 'error' key
    """
    result = send_sms(
        to=to_phone,
        from_phone=from_phone,
        text=message_text,
        consent=consent_type
    )
    
    if result:
        if isinstance(result, list) and len(result) > 0:
            if result[0].get('status') == 'rejected':
                return {'success': False, 'error': f"Rejected: {result[0].get('reject_reason', 'Unknown reason')}"}
        return {'success': True, 'data': result}
    
    return {'success': False, 'error': 'Failed to send SMS'}


# Main execution
if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('MANDRILL_API_KEY'):
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        exit(1)
    
    print('📱 Sending SMS...')
    print('')
    
    # Check for custom message from environment (set by web UI)
    custom_message = os.getenv('SMS_CUSTOM_MESSAGE')
    custom_to = os.getenv('SMS_CUSTOM_TO')
    
    if custom_message or custom_to:
        result = send_sms(
            to=custom_to or os.getenv('SMS_TO_PHONE'),
            text=custom_message or os.getenv('SMS_MESSAGE')
        )
    else:
        result = send_sms()
    
    if result:
        print('\n✅ SMS operation completed!')
    else:
        print('\n❌ SMS operation failed!')
        exit(1)

