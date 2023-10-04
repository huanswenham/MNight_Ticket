import os
import pandas as pd
import qrcode

from customer import Customer


def generate_qrcodes_and_customers():
    customers = []

    data_file = os.getenv("OLD_CSV_FILE_PATH", default=None)
    file_name_title = os.getenv("FILE_NAME_TITLE", default="")

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
        qrpath = f"qrcodes/{login}{'_' + file_name_title if file_name_title else ''}_{order_no}.png"
        pdfpath = f"etickets/{login}{'_' + file_name_title if file_name_title else ''}_{order_no}_eticket.pdf"

        customers.append(Customer(order_no, firstname, surname, login, email, qrpath, pdfpath, product, quantity))

        data = f'''{order_no}'''

        img = qrcode.make(data)
        img.save(qrpath, scale="5")
    
    return customers