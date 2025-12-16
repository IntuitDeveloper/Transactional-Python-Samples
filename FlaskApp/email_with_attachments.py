"""
Send Email with Attachments using Mandrill API

This script demonstrates how to attach files to emails sent via
Mailchimp Transactional (Mandrill).

Usage:
    python email_with_attachments.py

Requirements:
    - mailchimp-transactional
    - python-dotenv
"""

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
    """
    Helper to read a local file and return a Base64 string.

    Args:
        file_path: Path to the file to read

    Returns:
        Base64-encoded string of the file contents
    """
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f'Warning: File not found: {file_path}')
        return None


def send_with_attachments():
    """
    Send an email with file attachments.
    """
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
        f'This file was created using Python.\n'
    )
    attachments.append({
        'type': 'text/plain',
        'name': 'readme.txt',
        'content': base64.b64encode(text_content.encode('utf-8')).decode('utf-8')
    })

    message = {
        'html': '''
            <h1>Your Documents</h1>
            <p>Please find the attached files for your review.</p>
            <ul>
                <li>Sample PDF document</li>
                <li>Readme text file</li>
            </ul>
        ''',
        'text': 'Your documents are attached. Please review them at your convenience.',
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
        'attachments': attachments,
        'tags': ['attachments', 'outbound-documents']
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('Email with attachments sent successfully!')
        print('=' * 50)
        print(f'Number of attachments: {len(attachments)}')

        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
                if r.get('_id'):
                    print(f"  Message ID: {r['_id']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
        return result

    except ApiClientError as error:
        print('Error sending email with attachments!')
        print('=' * 50)
        print(f'Mandrill API Error: {error.text}')
        print('=' * 50)
        return None


def send_csv_attachment():
    """
    Send an email with a dynamically created CSV attachment.
    """
    # Create CSV content
    csv_content = "Name,Email,Status,Joined\n"
    csv_content += "John Smith,john@example.org,Active,2024-01-15\n"
    csv_content += "Jane Doe,jane@example.org,Active,2024-02-20\n"
    csv_content += "Bob Johnson,bob@example.org,Pending,2024-03-10\n"

    attachments = [{
        'type': 'text/csv',
        'name': 'user_report.csv',
        'content': base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    }]

    message = {
        'html': '<h1>User Report</h1><p>Please find the attached CSV report.</p>',
        'text': 'User Report - CSV file attached.',
        'subject': 'User Report - CSV Attached',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': 'Report Service',
        'to': [
            {
                'email': os.getenv('DEFAULT_TO_EMAIL', 'recipient@example.org'),
                'type': 'to'
            }
        ],
        'attachments': attachments,
        'tags': ['report', 'csv']
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('CSV report email sent successfully!')

        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
        return result

    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


def send_json_attachment():
    """
    Send an email with a JSON attachment.
    """
    import json

    # Create JSON data
    data = {
        'status': 'success',
        'total_users': 42,
        'active_users': 38,
        'timestamp': datetime.now().isoformat(),
        'users': [
            {'name': 'John', 'email': 'john@example.org'},
            {'name': 'Jane', 'email': 'jane@example.org'}
        ]
    }

    json_content = json.dumps(data, indent=2)

    attachments = [{
        'type': 'application/json',
        'name': 'data.json',
        'content': base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
    }]

    message = {
        'html': '<h1>API Response Data</h1><p>JSON data file attached.</p>',
        'subject': 'API Data Export',
        'from_email': os.getenv('DEFAULT_FROM_EMAIL', 'test@example.org'),
        'from_name': os.getenv('DEFAULT_FROM_NAME', 'Data Export Service'),
        'to': [{'email': os.getenv('DEFAULT_TO_EMAIL', 'test@example.org'), 'type': 'to'}],
        'attachments': attachments,
        'tags': ['api', 'json']
    }

    try:
        result = mailchimp.messages.send({'message': message})

        print('JSON attachment email sent successfully!')

        if isinstance(result, list):
            for r in result:
                print(f"{r['email']}: {r['status']}")
        else:
            print(f'Unexpected result structure: {result}')

        print('=' * 50)
        return result

    except ApiClientError as error:
        print(f'Error: {error.text}')
        return None


if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('MANDRILL_API_KEY'):
        print('Error: MANDRILL_API_KEY not found in environment variables!')
        print('Please create a .env file with your Mandrill API key.')
        exit(1)

    print('Sending email with attachments...\n')
    send_with_attachments()

    # Uncomment to test CSV attachment
    # print('\n\nSending CSV attachment...\n')
    # send_csv_attachment()

    # Uncomment to test JSON attachment
    # print('\n\nSending JSON attachment...\n')
    # send_json_attachment()
