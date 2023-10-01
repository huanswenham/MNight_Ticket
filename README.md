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

### .env
Create a .env file. Below are the contents required to be filled in this file:

```.env
OLD_CSV_FILE_PATH=
NEW_CSV_FILE_PATH=
FILE_NAME_TITLE=
SENDER_EMAIL=
SENDER_PASSWORD=
QRCODE_PAGE_BACKGROUND_FILE_PATH=
QRCODE_HAS_TRANSPARENT_BACKGROUND=
QRCODE_BACKGROUND_RGBA_COLOR=
QRCODE_X_SIZE_SCALE=
QRCODE_Y_SIZE_SCALE=
QRCODE_X_OFFSET=
QRCODE_Y_OFFSET=
GOOGLE_SHEET_NAME=
```

- <span style="color:#4169E1"> OLD_CSV_FILE_PATH </span>: Path to the old data csv file to cross check with the new file in order to prevent sending out e-tickets that have already been sent out before.
- <span style="color:#4169E1"> NEW_CSV_FILE_PATH </span>: Path to the new data csv file to generate and send new e-tickets.
- <span style="color:#4169E1"> FILE_NAME_TITLE (Optional) </span>: Name of the e-tickets will be in the format of "{login}_{FILE_NAME_TITLE}\_{order no}_eticket.pdf"
- <span style="color:#4169E1"> SENDER_EMAIL </span>: Email that is responsible for sending the etickets.
- <span style="color:#4169E1"> SENDER_PASSWORD </span>: Password for the email account that is responsible for sending the etickets.
- <span style="color:#4169E1"> QRCODE_PAGE_BACKGROUND_FILE_PATH </span>: Path to pdf file for e-ticket background design.
- <span style="color:#4169E1"> QRCODE_HAS_TRANSPARENT_BACKGROUND </span>: <span style="color:	#00FA9A">[Boolean]</span> Value will be "True" if the qrcode requires a transparent background, "False" otherwise.
- <span style="color:#4169E1"> QRCODE_BACKGROUND_RGBA_COLOR </span>: Color in the format of "{R} {G} {B} {Alpha}" for background of qrcode (ex: 12 210 232 255).
- <span style="color:#4169E1"> QRCODE_X_SIZE_SCALE </span>: <span style="color:	#00FA9A">[Float]</span> Horizontal scaling for qrcode.
- <span style="color:#4169E1"> QRCODE_Y_SIZE_SCALE </span>: <span style="color:	#00FA9A">[Float]</span> Vertical scaling for qrcode.
- <span style="color:#4169E1"> QRCODE_X_OFFSET </span>: <span style="color:	#00FA9A">[Int]</span> Horizontal pixel offset from center.
- <span style="color:#4169E1"> QRCODE_Y_OFFSET </span>: <span style="color:	#00FA9A">[Int]</span> Vertical pixel offset from center.
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

## Usage
Configure the values for your .env file to suite your use case. Simply run main.py to execute the program.

> [!WARNING]
> Do note that you might need to do several test runs using dummy data to tweak the scale and offset for the qrcode on the e-ticket.

All newly generated qrcodes appear under the qrcodes folder, and the newly generated e-ticket pdfs will appear under the e-tickets folder.