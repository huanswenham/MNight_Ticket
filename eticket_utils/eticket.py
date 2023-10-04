import os
from PIL import Image

from eticket_utils import pdf_csv, qrcode


def generate_etickets(customers):
    """Generates e-tickets for list of customers provided.

    Args:
        customers (List[Customer]): New customers.
    """
    data_file = os.getenv("OLD_CSV_FILE_PATH", default=None)
    
    for c in customers:
        qrcode.modify_qrcode(c.qrpath)
        _create_eticket(c.qrpath)
        pdf_csv.put_pdf_path_to_csv(c.ordernum, c.pdfpath, data_file)


def _create_eticket(ImageFilePath):
    qrcode_background_fp = os.getenv("QRCODE_PAGE_BACKGROUND_FILE_PATH", default=None)

    x_scale = float(os.getenv("QRCODE_X_SIZE_SCALE", default="0"))
    y_scale = float(os.getenv("QRCODE_Y_SIZE_SCALE", default="0"))
    x_offset = int(os.getenv("QRCODE_X_OFFSET", default="0"))
    y_offset = int(os.getenv("QRCODE_Y_OFFSET", default="0"))

    background = Image.open(qrcode_background_fp)
    w, h = background.size[0], background.size[1]

    filehead = (str(ImageFilePath).split(".png")[0]).split("/")[1]

    qr = Image.open(ImageFilePath)
    new_qr = qr.resize((round(qr.size[0] * x_scale), round(qr.size[1] * y_scale)))

    e_ticket = Image.new('RGB', background.size, (250,250,250))
    e_ticket.paste(background, (0,0))

    offset = (int(round(((w - new_qr.size[0]) / 2), 0)) + x_offset, int(round(((h - new_qr.size[1]) / 2))) + y_offset)
    e_ticket.paste(new_qr, offset, new_qr)
    e_ticket.save(f"etickets/{filehead}_eticket.pdf")