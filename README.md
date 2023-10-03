![Python version](https://img.shields.io/badge/python-3.11-blue)

# MNight Ticket

MNight Ticket is an e-ticket pdf generating and mail sending system that was initially used for Imperial College Malaysian Society MNight 2022 e-tickets, but has since been adapted for broader applications.

## Setup

It is adviced that a virtual environment is setup. Before setting up, make sure that you have the correct Python version installed.

To setup and activate your virtual environment:

```bash
python -m venv venv
source venv/bin/activate 
```

To install all dependencies:

```bash
pip install -r requirements.txt
```

A few more files would be needed to complete the setup:
- .env
- creds.json
- content.txt
- values.json

### .env
Create a .env file. Copy the following into the new .env file:

```ini
# Purchase Order Data
OLD_CSV_FILE_PATH=
NEW_CSV_FILE_PATH=

# E-Ticket Data
FILE_NAME_TITLE=
QRCODE_PAGE_BACKGROUND_FILE_PATH=
QRCODE_HAS_TRANSPARENT_BACKGROUND=
QRCODE_BACKGROUND_RGBA_COLOR=
QRCODE_X_SIZE_SCALE=
QRCODE_Y_SIZE_SCALE=
QRCODE_X_OFFSET=
QRCODE_Y_OFFSET=

# Email Sending Data
SENDER_EMAIL=
SENDER_PASSWORD=
EMAIL_SUBJECT=
EMAIL_TITLE_IMG=
EMAIL_CONTENT=email_templates/content.txt  # this value shouldn't change, just change the text in content.txt
EMAIL_VALUES=email_templates/values.json  # this value shouldn't change, just change the data in values.json

# Google Sheet Record Data
GOOGLE_SHEET_NAME=
```

Most of these fields are required to be filled with values. Here is a detailed explaination for the functionality of all the fields and the values they require:

#### 1. Purchase Order Data
- <span style="color:#4169E1"> OLD_CSV_FILE_PATH </span>: Path to the old data csv file to cross check with the new file in order to prevent sending out e-tickets that have already been sent out before.
- <span style="color:#4169E1"> NEW_CSV_FILE_PATH </span>: Path to the new data csv file to generate and send new e-tickets.

#### 2. E-Ticket Data
- <span style="color:#4169E1"> FILE_NAME_TITLE (Optional) </span>: Name of the e-tickets will be in the format of "{login}_{FILE_NAME_TITLE}\_{order no}_eticket.pdf"
- <span style="color:#4169E1"> QRCODE_PAGE_BACKGROUND_FILE_PATH </span>: Path to image file for e-ticket background design.
- <span style="color:#4169E1"> QRCODE_HAS_TRANSPARENT_BACKGROUND </span>: <span style="color:	#00FA9A">[Boolean]</span> Value will be "True" if the qrcode requires a transparent background, "False" otherwise.
- <span style="color:#4169E1"> QRCODE_BACKGROUND_RGBA_COLOR </span>: Color in the format of "{R} {G} {B} {Alpha}" for background of qrcode (ex: 12 210 232 255).
- <span style="color:#4169E1"> QRCODE_X_SIZE_SCALE </span>: <span style="color:	#00FA9A">[Float]</span> Horizontal scaling for qrcode.
- <span style="color:#4169E1"> QRCODE_Y_SIZE_SCALE </span>: <span style="color:	#00FA9A">[Float]</span> Vertical scaling for qrcode.
- <span style="color:#4169E1"> QRCODE_X_OFFSET </span>: <span style="color:	#00FA9A">[Int]</span> Horizontal pixel offset from center.
- <span style="color:#4169E1"> QRCODE_Y_OFFSET </span>: <span style="color:	#00FA9A">[Int]</span> Vertical pixel offset from center.

#### 3. Email Sending Data
- <span style="color:#4169E1"> SENDER_EMAIL </span>: Email that is responsible for sending the e-tickets.
- <span style="color:#4169E1"> SENDER_PASSWORD </span>: Password for the email account that is responsible for sending the e-tickets.
- <span style="color:#4169E1"> EMAIL_SUBJECT </span>: Subject for the email.
- <span style="color:#4169E1"> EMAIL_TITLE_IMG </span>: Header image for email (must be in dimension 800px X 200px).
- <span style="color:#4169E1"> EMAIL_CONTENT </span>: Path of text file for content of email (default as "email_templates/content.txt", detailed guide on text format for content.txt can be found at a later point within this document).
- <span style="color:#4169E1"> EMAIL_VALUES </span>: Path of json file for values to be replaced in text file provided in EMAIL_CONTENT (default as "email_templates/values.json", detailed guide on json format for values.json can be found at a later point within this document).

#### 4. Google Sheet Data
- <span style="color:#4169E1"> GOOGLE_SHEET_NAME </span>: Name of the google sheet to record data.


### creds.json
Create a creds.json file. Copy the creds from google application setup into this file, the format looks something like this:

```json
{
  "type": ,
  "project_id": ,
  "private_key_id": ,
  "private_key": ,
  "client_email": ,
  "client_id": ,
  "auth_uri": ,
  "token_uri": ,
  "auth_provider_x509_cert_url": ,
  "client_x509_cert_url":
}
```

### content.txt
Located inside "email_templates" folder. The format for the text is heavily based on HTML. Here is an example:
```txt
<p>Dear {name},</p>
<br>
<p>Thank you for purchasing your ticket for Welcome Dinner. Your ticket is attached in this email. 
This ticket is valid to be scanned for <b>{quantity} time(s)</b> on the <b>{date}.</b></p>

<p>We will be having a <b>Welcome Reception</b> which will run from <b>5pm to approximately 6.30pm</b> before the dinner, 
so we will have time to travel to Aroma Buffet together. Feel free to email events.icums@gmail.com if you have any queries.</p>

<p>Follow <a href="https://www.instagram.com/icu.ms/" target="_blank" rel="noopener noreferrer">@icu.ms</a> on Instagram to receive updates on future. 
See you very soon!</p>
<br>
<p>
Kind regards,
<br>
Events Officer
<br>
Imperial College Union Malaysian Society
</p>
```

- All new lines and tabs will be ignored, however spaces will remain.
- Use "\<br>" tags for new lines or add more space between paragraphs.
- Start each paragraph with "\<p>" and end them with "\</p>". They will provide some default spacing between paragraphs.
- To bold text, place them inside "\<b>" and "\</b>" tag.
- To make a link, use the format: \<a href="{LINK URL}" target="_blank" rel="noopener noreferrer">{TEXT FOR LINK}\</a>
- For values to be replaced, wrap the key with curly braces (ex: {name}). Values for "name" and "quantity" keys are readily provided by this system, so just use them wherever it is required in content.txt without needing to define a value for them. Other keys will be replaced by the values defined in the json file provided at EMAIL_VALUES in .env before the email is sent.

### values.json
Located inside "email_templates" folder. The data is in a JSON format with every key defined mapping to a value. Example:
```json
{
  "date": "6th of October 2023",
  "event_title": "Welcome Dinner 2023"
}
```
The system will find all keys in the format of {KEY} in content.txt and replace with it's corresponding value defined in this file before sending the email.


## Usage
Configure the values for your .env file to suite your use case. Simply run main.py to execute the program.

> [!WARNING]
> Do note that you might need to do several test runs using dummy data to tweak the scale and offset for the qrcode on the e-ticket.

All newly generated qrcodes appear under the qrcodes folder, and the newly generated e-ticket pdfs will appear under the e-tickets folder.