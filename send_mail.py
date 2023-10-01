import os
import yagmail
from read_mail import read_mail

def send_mail(customers, config):
    email = config["EMAIL"]
    pwd = config["PASSWORD"]
    subject = config["SUBJECT"]
    mailer = yagmail.SMTP(email, pwd)

    for c in customers:
        email = read_mail(c.firstname, c.surname, c.quantity, c.product)
        try:
            mailer.send(to=c.email,
            subject=subject,
            contents=email,
            attachments=[c.pdfpath])

            print("Succesfully sent to " + c.firstname + " " + c.surname)
        except:
            print("FAILED to send to " + c.firstname + " " + c.surname)