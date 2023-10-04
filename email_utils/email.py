import os
import yagmail

from email_utils import content
from googlesheet import googlesheet

def send_email_and_append_gsheet(customers, mailer, sheet):
    subject = os.getenv('EMAIL_SUBJECT', default="")

    for c in customers:
        # read content from EMAIL_CONTENT file provided and send email
        _send_email(c, mailer, subject)

        # write newly created customer entry into Google Sheet
        googlesheet.write_new_entry(c, sheet)



def _send_email(customer, mailer, subject):
    """Send email to customer provided with newly generated e-ticket as attachment.
    Content of email will be compiled from file stated in EMAIL_CONTENT field from .env file.

    Args:
        customers (List[Customer]): New customers.
    """
    
    email = content.compile_email_content(customer.firstname, customer.surname, customer.quantity)
    try:
        mailer.send(to=customer.email,
        subject=subject,
        contents=email,
        attachments=[customer.pdfpath])

        print("Succesfully sent to " + customer.firstname + " " + customer.surname)
    except:
        print("FAILED to send to " + customer.firstname + " " + customer.surname)