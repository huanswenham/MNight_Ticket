import os
import pandas as pd
import qrcode
from PIL import Image

from customer.customer import Customer


def generate_qrcodes_and_customers():
    """Generates new qrcodes and creates new customers list

    Returns:
        List[Customer]: New customers for e-ticket generation.
    """
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


def modify_qrcode(ImageFilePath):
    rgba = (255, 255, 255, 0)
    qrcode_has_transparent_background = os.getenv("QRCODE_HAS_TRANSPARENT_BACKGROUND", default=True)

    if not eval(qrcode_has_transparent_background):
        rgba = _process_env_color()
    
    qrcode = Image.open(ImageFilePath, 'r')
    qr_rgba = qrcode.convert("RGBA")
    datas = qr_rgba.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append(rgba)
        else:
            newData.append(item)

    qr_rgba.putdata(newData)
    qr_rgba.save(ImageFilePath)


def _process_env_color():
    color = os.getenv("QRCODE_BACKGROUND_RGBA_COLOR", default=None)
    rgba_ls = color.split(" ")
    for i, value in enumerate(rgba_ls):
        rgba_ls[i] = int(value)
    return tuple(rgba_ls)