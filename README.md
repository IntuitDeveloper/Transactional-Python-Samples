# Mailchimp Transactional API Demo (Flask)

A sample Flask web application demonstrating how to send transactional emails using the Mailchimp Transactional (Mandrill) API. Features include sending single emails, emails with merge tags, attachments, templates, and a "kitchen sink" demo with all features.

For more focused problem solving using python, refer to the use-cases as mentioned in [README_USECASES_PYTHON.md](FlaskApp/README_USECASES_PYTHON.md)

---

## Features
- Send a single email to a recipient
- Send emails with personalized merge tags
- Send emails with file attachments (PDF, text)
- Send emails using pre-defined templates
- Kitchen sink: demo of all features (attachments, merge tags, images, etc.)
- Dynamic web UI for selecting and testing features

---

## Requirements
- Python 3.8+
- pip (Python package manager)
- Mailchimp Transactional (Mandrill) API key

### Python Packages
- Flask
- mailchimp_transactional
- python-dotenv

All dependencies are listed in `requirements.txt`.

---

## Installation

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd Transactional-Python-Samples
   python3 -m venv venv
   source venv/bin/activate  
   cd FlaskApp
   ```

2. **Install dependencies**
   ```sh
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**
   ```sh
   cp env.example .env
   # Edit .env with your Mandrill API key and email settings
   ```
   
   The `.env` file should contain:
   ```env
   MANDRILL_API_KEY=your-mailchimp-transactional-api-key
   DEFAULT_FROM_EMAIL=your-from-email@example.com
   DEFAULT_FROM_NAME="Your Name"
   DEFAULT_TO_EMAIL=recipient@example.com
   DEFAULT_TO_NAME="Recipient Name"
   ```
   
   > **Note:** Always quote values that contain spaces or special characters.

4. **(Optional) Add sample attachments**
   - Place a `sample.pdf` file in the `FlaskApp` directory for attachment demos.
   - Place images (e.g., `logo.png`) in `FlaskApp/static/images/` for inline image demos.

---

## Running the Application

1. **Start the Flask server**
   ```sh
   python3 app.py
   ```
   - The app will run on `http://0.0.0.0:5002` by default.

2. **Open your browser**
   - Navigate to `http://localhost:5002` to access the web UI.

---

## API Documentation

### Main Endpoints

- `/` : Main web UI for selecting and running email scripts.
- `/testEmailbasedOnScriptID` : Handles form submissions to trigger email sending based on selected script.
- `/createTemplate` : Creates a new Mailchimp template if it does not exist (used internally by the UI).

### Email Scripts (selectable from UI)
- **script1**: Send a single email
- **script2**: Send email with merge tags (requires first name, last name, company, membership level)
- **script3**: Send email with attachments (uses sample.pdf and a generated text file)
- **script4**: Send email using a template (choose template in UI)
- **script5**: Kitchen sink (all features: merge tags, attachments, images, etc.)

---

## Software Versions
- Python: 3.8+
- Flask: 2.x+
- mailchimp_transactional: 1.x+
- python-dotenv: 1.x+

---

## Project Structure
```
FlaskApp/
├── app.py                # Main Flask application
├── config.py             # Configuration and environment variables
├── requirements.txt      # Python dependencies
├── static/
│   ├── styles.css        # Custom CSS
│   └── images/           # Image assets (e.g., logo.png)
├── templates/
│   └── index.html        # Main web UI template
└── sample.pdf            # (Optional) Sample PDF for attachments
```

---

## Notes
- Make sure your Mailchimp Transactional API key is active and has permission to send emails.
- All email addresses used must be verified in your Mailchimp account (if required by your plan).
- For demo purposes, all default values are loaded from `config.py` or `.env`.

---

## License
See `LICENSE.txt` for license information.
