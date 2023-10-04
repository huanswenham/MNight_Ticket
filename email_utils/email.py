import os
import yagmail

from email_utils import content

def send_email(customers):
    email = os.getenv('SENDER_EMAIL', default=None)
    pwd = os.getenv('SENDER_PASSWORD', default=None)
    subject = os.getenv('EMAIL_SUBJECT', default="")
    mailer = yagmail.SMTP(email, pwd)

    for c in customers:
        email = content.compile_email_content(c.firstname, c.surname, c.quantity)
        try:
            mailer.send(to=c.email,
            subject=subject,
            contents=email,
            attachments=[c.pdfpath])

            print("Succesfully sent to " + c.firstname + " " + c.surname)
        except:
            print("FAILED to send to " + c.firstname + " " + c.surname)