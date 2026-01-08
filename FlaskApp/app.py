"""
Mailchimp Transactional API Demo Flask Application

Technical Documentation:
- This Flask app demonstrates sending transactional emails using the Mailchimp Transactional (Mandrill) API.
- Features include sending single emails, emails with merge tags, attachments, templates, and a kitchen sink demo.
- Uses environment variables (via config.py) for API keys and email addresses.
- Provides a web UI for selecting and testing different email features.

User Documentation:
- Start the app and open the web UI to test different email-sending features.
- Configure your API key and email addresses in the .env file or config.py.
- Use the UI to select a script, fill in required fields, and send test emails.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from config import MANDRILL_API_KEY, DEFAULT_FROM_EMAIL, DEFAULT_FROM_NAME, DEFAULT_TO_EMAIL, DEFAULT_TO_NAME
from email_with_template import TEMPLATES
import requests
import urllib.parse
import json
from functools import wraps


def template_exists(template_name):
    """
    Check if a template exists in Mandrill.
    Uses MANDRILL_API_KEY from config.py for consistency.
    """
    try:
        client = MailchimpTransactional.Client(MANDRILL_API_KEY)
        # Call without the label parameter for simpler request
        templates = client.templates.list()
        
        # Debug: print what we're getting back
        print(f"DEBUG templates type: {type(templates)}")
        if templates:
            print(f"DEBUG first item type: {type(templates[0]) if len(templates) > 0 else 'empty'}")
        
        # Handle case where API returns bytes
        if isinstance(templates, bytes):
            templates = json.loads(templates.decode('utf-8'))
        elif isinstance(templates, str):
            templates = json.loads(templates)
        
        # Now iterate
        if isinstance(templates, list):
            for t in templates:
                # Handle if individual items are bytes/str
                if isinstance(t, (bytes, str)):
                    t = json.loads(t if isinstance(t, str) else t.decode('utf-8'))
                if isinstance(t, dict) and t.get('name') == template_name:
                    return True
        return False
    except ApiClientError as e:
        print(f"API Error checking template: {e}")
        return False
    except Exception as e:
        print(f"Error checking template existence: {e}")
        return False

app = Flask(__name__, 
    static_folder='static',
    static_url_path='/static',
    template_folder='templates')

# Set a secret key for session and flash
# In production, use a secure random key from environment variables
import os
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

@app.before_request
def clear_session():
    if request.endpoint == 'index':
        # Clear all flash messages
        if '_flashes' in session:
            del session['_flashes']

@app.route('/')
def index():
    return render_template('index.html')

def send_email_with_merge_tags():
    """
    Send a personalized welcome email using Mailchimp Transactional API with merge tags.

    Technical Documentation:
    - This function constructs an email message with both HTML and plain text bodies, using Handlebars merge tags for personalization.
    - Merge tags are populated from form data submitted by the user (first name, last name, company name, membership level).
    - The function uses global_merge_vars for company-wide variables and merge_vars for recipient-specific variables.
    - The email is sent to the default recipient as configured in config.py.
    - The function returns a status message for each recipient or an error message if the API call fails.
    """
    try:
        # Initialize the Mailchimp Transactional API client
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        # Construct the message payload with merge tags for personalization
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
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            'headers': {
                'Reply-To': DEFAULT_FROM_EMAIL
            },
            'global_merge_vars': [
                {'name': 'company_name', 'content': request.form.get('companyName', 'Intuit Developer Program')},
                {'name': 'membership_level', 'content': request.form.get('membershipLevel', 'Premium')},
            ],
            'merge_vars': [
                {
                    'rcpt': DEFAULT_TO_EMAIL,
                    'vars': [
                        {'name': 'fname', 'content': request.form.get('firstName', 'John')},
                        {'name': 'lname', 'content': request.form.get('lastName', 'Smith')}
                    ]
                }
            ],
            'merge_language': 'handlebars'
        }
        # Send the email using the Mailchimp API
        result = mailchimp.messages.send({"message": message})
        print('Email sent successfully:', message)
        print('Full result:', result)
        if isinstance(result, list):
            status_lines = [f"send_email_with_merge_tags to : {recipient['email']}: {recipient['status']}" for recipient in result]
            return '<br>'.join(status_lines)
        else:
            return f"Unexpected result structure: {result}"
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"

def send_email_with_attachments():
    """
    Send an email with file attachments using Mailchimp Transactional API.

    Technical Documentation:
    - Reads a sample PDF file (if present) and a generated text file, encodes them in base64, and attaches them to the email.
    - Constructs the message payload with attachments and sends it to the default recipient.
    - Returns a status message for each recipient or an error message if the API call fails.

    User Documentation:
    - Use this function to send an email with attached files (sample.pdf and a generated readme.txt).
    - If sample.pdf is not present, only the text file will be attached.
    - The email will be sent to the default recipient as configured in config.py.
    - A status message will be displayed for each recipient, or an error if the send fails.
    """
    import base64
    import os
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        # Read sample.pdf as base64 if it exists
        pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
        print(pdf_path + " pdf_path")
        pdf_content = ''
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode('utf-8')
        # Create a text file attachment as base64
        text_content = 'This is a demo text file created by the Mandrill Use Case File.\n\nGenerated at: ' + __import__('datetime').datetime.utcnow().isoformat()
        text_base64 = base64.b64encode(text_content.encode('utf-8')).decode('utf-8')
        attachments = []
        if pdf_content:
            attachments.append({
                'type': 'application/pdf',
                'name': 'sample.pdf',
                'content': pdf_content
            })
        attachments.append({
            'type': 'text/plain',
            'name': 'readme.txt',
            'content': text_base64
        })
        message = {
            'html': '<h1>Your Documents</h1><p>Please find the attached files.</p>',
            'text': 'Your documents are attached.',
            'subject': 'Documents Attached',
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            'attachments': attachments,
            'tags': ['attachments', 'outbound-documents']
        }
        result = mailchimp.messages.send({"message": message})
        print('Email sent successfully:', message)
        print('Full result:', result)
        if isinstance(result, list):
            status_lines = [f"{r['email']}: {r['status']}" for r in result]
            return '<br>'.join(status_lines)
        else:
            return f"Unexpected result structure: {result}"
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"


@app.route('/testEmailbasedOnScriptID', methods=['POST'])
def testEmailbasedOnScriptID():    
    """
    Flask route to handle form submissions for sending emails based on the selected script.

    Technical Documentation:
    - Receives POST requests from the main form, determines which email function to call based on the selected script.
    - Calls the appropriate function (send_single_email, send_email_with_merge_tags, etc.) and passes the result to the template for display.
    - Handles invalid script selection with a flash message and redirects to the index page.

    User Documentation:
    - Use this endpoint to trigger different email-sending scripts from the web UI.
    - Select the desired script in the form and submit; the result will be shown on the main page.
    - If an invalid script is selected, an error message will be displayed.
    """
    #get form data and call respective function
    if request.method == 'POST':
        form_data = request.form
        script_name = form_data['Script_name']
        print("In testEmailbasedOnScriptID........" +script_name)

        script_run_status = ''
        if script_name == 'single':
            script_run_status = send_single_email()
        elif script_name == 'mergeTags':
            script_run_status = send_email_with_merge_tags()
        elif script_name == 'attachments':
            script_run_status = send_email_with_attachments()
        elif script_name == 'templates':
            script_run_status = send_email_with_template()
        elif script_name == 'allInOne':
            script_run_status = send_bulk_email()
        else:
            flash('Invalid script selected. Please try again.', 'error')
            return redirect(url_for('index'))
        return render_template('index.html', script_run_status=script_run_status)
    else:
        return render_template('index.html')
       
def send_single_email():
    """
    Send a simple transactional email using Mailchimp Transactional API.

    Technical Documentation:
    - Constructs a basic email message with HTML and plain text bodies.
    - Sends the email to the default recipient as configured in config.py.
    - Returns a status message with the result or an error message if the API call fails.

    User Documentation:
    - Use this function to send a basic test email to verify Mailchimp Transactional API integration.
    - The email will be sent to the default recipient and will contain a simple greeting.
    - The result will display the status, recipient, and message ID.
    """
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        message = {
            'html': '<p>Hello HTML world! from Mailchimp transactional API Demo</p>',
            'text': 'Hello plain world! from Mailchimp transactional API Demo',
            'subject': 'Hello world',
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            'headers': {
                'Reply-To': DEFAULT_FROM_EMAIL
            }
        }
        result = mailchimp.messages.send({"message": message})
        print('Email sent successfully:', message)
        print('Full result:', result)
        if result and len(result) > 0:
            status_msg = f"Status: {result[0]['status']}<br>Email to: {result[0]['email']}<br>Message ID: {result[0]['_id']}"
        else:
            status_msg = f"Unexpected result structure: {result}"
        return status_msg
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"

def send_bulk_email():
    """
    Send a bulk/kitchen-sink email demonstrating multiple Transactional API features.

    Technical Documentation:
    - Prepares attachments (PDF and text file) and embeds an image if available.
    - Constructs a message with merge tags, attachments, images, and various tracking options.
    - Sends the email to the default recipient and returns a status message for each recipient.

    User Documentation:
    - Use this function to send a feature-rich email with attachments and embedded image.
    - The email demonstrates advanced Mandrill/Mailchimp Transactional API features.
    - The result will display the status for each recipient or an error if the send fails.
    """
    import base64
    import os
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        # Prepare attachments (reuse PDF and text file logic)
        attachments = []
        pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode('utf-8')
            attachments.append({
                'type': 'application/pdf',
                'name': 'sample.pdf',
                'content': pdf_content
            })
        text_content = 'This is a demo text file created by the Mandrill Use Case File.\n\nGenerated at: ' + __import__('datetime').datetime.utcnow().isoformat()
        text_base64 = base64.b64encode(text_content.encode('utf-8')).decode('utf-8')
        attachments.append({
            'type': 'text/plain',
            'name': 'readme.txt',
            'content': text_base64
        })
        # Prepare images (example: embed a logo if present)
        images = []
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_content = base64.b64encode(f.read()).decode('utf-8')
            images.append({
                'type': 'image/png',
                'name': 'logo.png',
                'content': logo_content
            })
        message = {
            'html': '''
                <h1>Hello {{fname}}!</h1>
                <p>This email demonstrates multiple Transactional API features.</p>
                <p>Company: {{company_name}}</p>
                <p>Account: {{account_id}}</p>
                <div style="width: 50px; height: 50px; background: #007bff; border: 2px solid #0056b3; display: inline-block;"></div>
            ''',
            'text': 'Hello {{fname}}!\n\nThis email demonstrates multiple Transactional API features.\nCompany: {{company_name}}\nAccount: {{account_id}}',
            'subject': 'Hello {{fname}} - Mandrill Features Demo',
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            # cc and bcc can be added as needed
            'headers': {
                'Reply-To': DEFAULT_FROM_EMAIL,
                'X-Custom-Header': 'Mandrill-Demo'
            },
            'global_merge_vars': [
                {'name': 'company_name', 'content': 'Intuit Developer Program'}
            ],
            'merge_vars': [
                {
                    'rcpt': DEFAULT_TO_EMAIL,
                    'vars': [
                        {'name': 'fname', 'content': 'John'},
                        {'name': 'account_id', 'content': 'ACC-001'}
                    ]
                }
            ],
            'merge_language': 'handlebars',
            'attachments': attachments,
            'images': images,
            'track_opens': True,
            'track_clicks': True,
            'auto_text': True,
            'auto_html': False,
            'inline_css': True,
            'tags': ['demo', 'kitchen-sink', 'features'],
            'metadata': {
                'campaign': 'mandrill-demo',
                'version': '1.0'
            },
            'important': True,
            'view_content_link': True,
            'preserve_recipients': False,
            'async': False
        }
        result = mailchimp.messages.send({"message": message})
        if isinstance(result, list):
            status_lines = [f"{r['email']}: {r['status']}" for r in result]
            return '<br>'.join(status_lines)
        else:
            return f"Unexpected result structure: {result}"
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"

def send_email_with_template():
    """
    Send an email using a Mailchimp Transactional template, creating the template if needed.

    Technical Documentation:
    - Retrieves the template name from the form, ensures the template exists (creates if not), and sends an email using that template.
    - Populates merge tags for personalization.
    - Returns a status message for each recipient or an error message if the API call fails.

    User Documentation:
    - Use this function to send a templated email, selecting the template via the web UI.
    - The template will be created if it does not already exist.
    - The result will display the status for each recipient or an error if the send fails.
    """
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        template_name = request.form['template_name']
        print("Selected template::::::: " + template_name)
        
        # Ensure the template exists, create if not available
        createTemplate(template_name)

        # Get template definition for mc:edit region name
        template_def = TEMPLATES.get(template_name, TEMPLATES['template1'])

        # Prepare template content by giving the actual data for the template
        message = {
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'subject': 'Welcome, {{fname}}',
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            'global_merge_vars': [
                {'name': 'company_name', 'content': 'Intuit Developer Program'}
            ],
            'merge_vars': [
                {
                    'rcpt': DEFAULT_TO_EMAIL,
                    'vars': [
                        {'name': 'fname', 'content': 'John'},
                        {'name': 'account_id', 'content': 'ACCOUNT-001'}
                    ]
                }
            ],
            'merge_language': 'handlebars',
            'tags': ['onboarding', 'welcome']
        }
        
        # Template content for mc:edit regions - use correct region name based on template
        if template_name == 'template1':
            template_content = [
                {
                    'name': 'welcome_message',
                    'content': "<hr><p>Thanks for joining <strong>{{company_name}}</strong>! We're excited to have you on board.</p><hr>This email is generated for pre-designed template, generated for template1<hr>"
                }
            ]
        else:
            template_content = [
                {
                    'name': 'goodbye_message',
                    'content': "<hr><p>We don't have much updates, but this email is for your account: {{account_id}} in company: {{company_name}}</p><hr>"
                }
            ]

        # Send the email using the specified template
        result = mailchimp.messages.send_template({
            'template_name': template_name,
            'template_content': template_content,
            'message': message
        })
        
        if isinstance(result, list):
            status_lines = [f"{r['email']}: {r['status']}" for r in result]
            return '<br>'.join(status_lines)
        else:
            return f"Unexpected result structure: {result}"
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"

def send_email_with_template_backup():
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        template_name = 'hello-template'
        message = {
            'from_email': DEFAULT_FROM_EMAIL,
            'from_name': DEFAULT_FROM_NAME,
            'subject': 'Welcome, {{fname}}',
            'to': [{
                'email': DEFAULT_TO_EMAIL,
                'name': DEFAULT_TO_NAME,
                'type': 'to'
            }],
            'global_merge_vars': [
                {'name': 'company_name', 'content': 'Intuit Developer Program'}
            ],
            'merge_vars': [
                {
                    'rcpt': DEFAULT_TO_EMAIL,
                    'vars': [
                        {'name': 'fname', 'content': 'John'},
                        {'name': 'account_id', 'content': 'ACC-001'}
                    ]
                }
            ],
            'merge_language': 'handlebars',
            'tags': ['onboarding', 'welcome']
        }
        template_content = [
            {
                'name': 'welcome_message',
                'content': "<hr><p>Thanks for joining <strong>{{company_name}}</strong>! We're excited to have you on board.</p><p><p><p><hr>This email is generated for pre-designed template.<hr>"
            }
        ]
        result = mailchimp.messages.send_template({
            'template_name': template_name,
            'template_content': template_content,
            'message': message
        })
        if isinstance(result, list):
            status_lines = [f"{r['email']}: {r['status']}" for r in result]
            return '<br>'.join(status_lines)
        else:
            return f"Unexpected result structure: {result}"
    except ApiClientError as error:
        return f"Mailchimp error: {error.__class__.__name__} - {error.text}"

@app.route('/createTemplate', methods=['POST'])
def createTemplate(templateName):
    """
    Create a new Mailchimp Transactional template if it does not already exist.
    If a template with the given name exists, a warning is flashed and no new template is created.
    Otherwise, creates a template with the appropriate subject, code, and text based on the template name.

    Args:
        templateName (str): The name of the template to create (e.g., 'template1', 'template2').

    Returns:
        None. Flashes a message to the user and prints the API response for debugging.
    """
    try:
        mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
        
        # Check if a template with the given name already exists
        if template_exists(templateName):
            flash(f'Template "{templateName}" already exists. No new template created.', 'warning')
        else:
            # Get template definition from shared TEMPLATES dict
            if templateName not in TEMPLATES:
                flash(f'Unknown template: {templateName}', 'error')
                return
            
            template_def = TEMPLATES[templateName]

            # Construct the template data payload for the API
            template_data = {
                'name': templateName,
                'from_email': DEFAULT_FROM_EMAIL,
                'from_name': DEFAULT_FROM_NAME,
                'subject': template_def['subject'],
                'code': template_def['code'],
                'text': template_def['text'],
                'publish': False,
                'labels': template_def['labels']
            }
            # Create the template using the Mailchimp API
            response = mailchimp.templates.add(template_data)
            print('Create Template Response:', response)
            flash(f'Template created: {response["name"]}', 'info')

    except ApiClientError as error:
        # Log the error for debugging
        print('An exception occurred while creating template: {}'.format(error.text))

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5002, debug=True)