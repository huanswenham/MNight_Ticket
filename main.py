# external packages
import os
import qrcode
import pandas as pd
from dotenv import load_dotenv

# internal imports
from customer import Customer
from validation import validations
from create_pdf import Reformat_QR, create_e_ticket
from embed_excel import embed_excel
from merge_excel import merge_excel
from send_mail import send_mail
from transfer_to_googlesheets import transfer


customers = []
shotcodes = []

google_sheet = None


#creating the qr code as image
def createQRCode(data_file, file_name_title):
    df = pd.read_csv(data_file)
    newDF = df[df['PDF'].isnull()]

    for _, values in newDF.iterrows():

        order_no = values["Order No"]
        firstname = values["First Name"]
        surname = values["Surname"]
        login = values["Login"]
        email = values["Email"]
        product = values["Product Name"]
        quantity = values["Quantity"]
        qrpath = f"qrcodes/{login}_{file_name_title}_{order_no}.png"
        pdfpath = f"etickets/{login}_{file_name_title}_{order_no}_eticket.pdf"

        customers.append(Customer(order_no, firstname, surname, login, email, qrpath, pdfpath, product, quantity))

        data = f'''{order_no}'''

        img = qrcode.make(data)
        img.save(qrpath, scale="5")


def foldersSetup():
    for f in ["qrcodes", "etickets"]:
        if not os.path.isdir(f):
            print(f"folder {f} does not exist, creating a {f} folder...")
            os.mkdir(f)


# Main
def main():
    load_dotenv()
    foldersSetup()

    # input validations
    if not validations.valid_env(): return
    google_sheet = validations.google_sheet_init()
    if not google_sheet: return

    data_file = os.getenv("OLD_CSV_FILE_PATH", default=None)
    new_file = os.getenv("NEW_CSV_FILE_PATH", default=None)
    file_name_title = os.getenv("FILE_NAME_TITLE", default="")

    merge_excel(data_file, new_file)

    createQRCode(data_file, file_name_title)

    for c in customers:
        Reformat_QR(c.qrpath)
        create_e_ticket(c.qrpath)
        embed_excel(c.ordernum, c.pdfpath, data_file)

    # send newly generated e-tickets via email
    config_dict = {
        'EMAIL': os.getenv('SENDER_EMAIL', default=None),
        'PASSWORD': os.getenv('SENDER_PASSWORD', default=None),
        'SUBJECT': os.getenv('EMAIL_SUBJECT', default="")
    }
    send_mail(customers, config_dict)
    transfer(customers, google_sheet)


# Run entire program
if __name__ == "__main__":
    main()