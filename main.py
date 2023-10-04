# external packages
from dotenv import load_dotenv

# internal imports
from setup import folders
from validations import validations
from csv_utils import merge_csv
from eticket_utils import qrcode, eticket
from email_utils import email
from googlesheet import googlesheet


def main():
    load_dotenv()

    # setup necessary folders
    folders.folders_setup()
    
    # input validations
    if not validations.valid_env(): return
    google_sheet = validations.google_sheet_init()
    if not google_sheet: return

    # merge data in new csv into old csv
    merge_csv.merge_to_old_csv()

    # generate new qrcodes and create new customers list
    customers = qrcode.generate_qrcodes_and_customers()

    # generate e-tickets from customers list
    eticket.generate_etickets(customers)

    # send newly generated e-tickets via email
    email.send_email(customers)

    # write newly created customer entries into Google Sheet
    googlesheet.write_new_data(customers, google_sheet)


# Run entire program
if __name__ == "__main__":
    main()