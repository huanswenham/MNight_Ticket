# external packages
import os
import qrcode
import pandas as pd
from dotenv import load_dotenv

# internal imports
from setup import folders
from validations import validations
from merge_csv import merge_csv
from eticket import qrcode
from create_pdf import Reformat_QR, create_e_ticket
from embed_excel import embed_excel
from send_mail import send_mail
from transfer_to_googlesheets import transfer



# Main
def main():
    load_dotenv()

    # setup necessary folders
    folders.folders_setup()
    
    # input validations
    if not validations.valid_env(): return
    google_sheet = validations.google_sheet_init()
    if not google_sheet: return

    data_file = os.getenv("OLD_CSV_FILE_PATH", default=None)

    merge_csv.merge_to_old_csv()

    customers = qrcode.generate_qrcodes_and_customers()

    for c in customers:
        Reformat_QR(c.qrpath)
        create_e_ticket(c.qrpath)
        embed_excel(c.ordernum, c.pdfpath, data_file)

    # # send newly generated e-tickets via email
    # config_dict = {
    #     'EMAIL': os.getenv('SENDER_EMAIL', default=None),
    #     'PASSWORD': os.getenv('SENDER_PASSWORD', default=None),
    #     'SUBJECT': os.getenv('EMAIL_SUBJECT', default="")
    # }
    # send_mail(customers, config_dict)
    # transfer(customers, google_sheet)


# Run entire program
if __name__ == "__main__":
    main()