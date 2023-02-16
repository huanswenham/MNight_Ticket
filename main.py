# import packages
import qrcode
import pandas as pd
from create_pdf import Reformat_QR, create_e_ticket
from embed_excel import embed_excel
from customer import Customer
from merge_excel import merge_excel
from send_mail import send_mail
from transfer_to_googlesheets import transfer


data_file = ''
new_file = ""
customers = []
shotcodes = []

QRCODE_TITLE = ""

#creating the qr code as image
def createQRCode():

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
        qrpath = f"qrcodes/{login}{QRCODE_TITLE}_{order_no}.png"
        pdfpath = f"e-tickets/{login}{QRCODE_TITLE}_{order_no}_eticket.pdf"

        customers.append(Customer(order_no, firstname, surname, login, email, qrpath, pdfpath, product, quantity))

        data = f'''{order_no}'''

        img = qrcode.make(data)
        img.save(qrpath, scale="5")



# Function to run the entire thing
# Yes, THE ENTIRE THING
def main():
    merge_excel(data_file, new_file)
    createQRCode()
    for c in customers:
        Reformat_QR(c.qrpath, c.product)
        create_e_ticket(c.qrpath, c.product)
        embed_excel(c.ordernum, c.pdfpath, data_file)
    print(pd.read_csv(data_file))

    config_file = open("config.txt")
    if config_file:
        config_details = config_file.read().split("\n")
        config_dict = {}
        for detail in config_details:
            detail_split = detail.split("=")
            config_dict[detail_split[0]] = detail_split[1]

        send_mail(customers, config_dict)
        transfer(customers)


# Run entire program
if __name__ == "__main__":
    main()