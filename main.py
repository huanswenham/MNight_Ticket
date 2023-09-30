# import packages
import os
import qrcode
import pandas as pd
from create_pdf import Reformat_QR, create_e_ticket
from embed_excel import embed_excel
from customer import Customer
from merge_excel import merge_excel
from send_mail import send_mail
from transfer_to_googlesheets import transfer
from dotenv import load_dotenv


customers = []
shotcodes = []

ENV_VAR_NULL_CHECK_LIST = [
    "OLD_CSV_FILE_PATH", 
    "NEW_CSV_FILE_PATH", 
    "GOOGLE_SHEET_NAME", 
    "SENDER_EMAIL", 
    "SENDER_PASSWORD",
    "QRCODE_PAGE_BACKGROUND_FILE_PATH",
    "QRCODE_HAS_TRANSPARENT_BACKGROUND",
    "QRCODE_BACKGROUND_RGBA_COLOR"
]


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
        pdfpath = f"e-tickets/{login}_{file_name_title}_{order_no}_eticket.pdf"

        customers.append(Customer(order_no, firstname, surname, login, email, qrpath, pdfpath, product, quantity))

        data = f'''{order_no}'''

        img = qrcode.make(data)
        img.save(qrpath, scale="5")


# ENV VALUES VALIDATION
def validEnvFields():
    for name, value in os.environ.items():
        if not value and name in ENV_VAR_NULL_CHECK_LIST:
            print(f"value for {name} not provided in .env file, please provide a value for this field.")
            return False
    
    if not validateColorEnvField(): return False

    return True


def validateColorEnvField():
    color = os.getenv("QRCODE_BACKGROUND_RGBA_COLOR", default=None)
    rgba_ls = color.split(" ")
    
    if not len(rgba_ls) == 4:
        print("Invalid rgba value for QRCODE_BACKGROUND_RGBA_COLOR provided in .env file, please use the format \'\{R value\} \{G value\} \{B value\} \{Alpha value\}\'")
        return False

    for value in rgba_ls:
        if not value.isdigit() or 0 > int(value) or int(value) > 255:
            print("Invalid RGBA values for QRCODE_BACKGROUND_RGBA_COLOR provided in .env file, please make sure each RGBA value is between 0 and 255")
            return False
    
    return True


# Function to run the entire thing
# Yes, THE ENTIRE THING
def main():
    load_dotenv()

    if not validEnvFields():
        return

    data_file = os.getenv("OLD_CSV_FILE_PATH", default=None)
    new_file = os.getenv("NEW_CSV_FILE_PATH", default=None)
    file_name_title = os.getenv("FILE_NAME_TITLE", default="")

    merge_excel(data_file, new_file)

    createQRCode(data_file, file_name_title)

    for c in customers:
        Reformat_QR(c.qrpath, c.product)
        create_e_ticket(c.qrpath, c.product)
        embed_excel(c.ordernum, c.pdfpath, data_file)
    print(pd.read_csv(data_file))

    # send newly generated e-tickets via email
    config_dict = {
        'EMAIL': os.getenv('SENDER_EMAIL', default=None),
        'PASSWORD': os.getenv('SENDER_PASSWORD', default=None)
    }
    send_mail(customers, config_dict)
    transfer(customers)


# Run entire program
if __name__ == "__main__":
    main()