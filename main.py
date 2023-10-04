# external packages
from dotenv import load_dotenv

# internal imports
from setup import folders
from validations import validations
from csv_utils import merge_csv
from eticket_gen import qrcode, eticket
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

    merge_csv.merge_to_old_csv()

    customers = qrcode.generate_qrcodes_and_customers()

    # generate e-tickets from customers list
    eticket.generate_etickets(customers)

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