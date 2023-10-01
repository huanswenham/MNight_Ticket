import os
from PIL import Image

ADDITIANAL_IMAGES = []


def process_env_color():
    color = os.getenv("QRCODE_BACKGROUND_RGBA_COLOR", default=None)
    rgba_ls = color.split(" ")
    for i, value in enumerate(rgba_ls):
        rgba_ls[i] = int(value)
    return tuple(rgba_ls)


def Reformat_QR(ImageFilePath, product):
    rgba = (255, 255, 255, 0)
    qrcode_has_transparent_background = os.getenv("QRCODE_HAS_TRANSPARENT_BACKGROUND", default=True)

    if not eval(qrcode_has_transparent_background):
        rgba = process_env_color()
    
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
    # w, h = qrcode.size
    # # if product == "MNight 2022 (5th March 2022)":
    # #     color = (255,212,232)
    # # else:
    # #     color = (248,252,251)
    # color = COLOR

    # for x in range(w):
    #     for y in range(h):
    #         current_color = qr_rgb.getpixel((x,y))
    #         if current_color == (255,255,255):
    #             qr_rgb.putpixel((x,y), color)
    # qr_rgb.save(ImageFilePath)


def create_e_ticket(ImageFilePath, product):
    images = ADDITIANAL_IMAGES

    qrcode_background_fp = os.getenv("QRCODE_PAGE_BACKGROUND_FILE_PATH", default=None)

    x_scale = float(os.getenv("QRCODE_X_SIZE_SCALE", default="0"))
    y_scale = float(os.getenv("QRCODE_Y_SIZE_SCALE", default="0"))
    x_offset = int(os.getenv("QRCODE_X_OFFSET", default="0"))
    y_offset = int(os.getenv("QRCODE_Y_OFFSET", default="0"))

    # if product == "MNight 2022 (5th March 2022)":
    #     background = Image.open("eticket_background_5th.png")
    #     w = background.size[0]
    #     h = background.size[1]
    # else:
    #     background = Image.open("eticket_background_6th.png")
    #     w = background.size[0]
    #     h = background.size[1]

    background = Image.open(qrcode_background_fp)
    w = background.size[0]
    h = background.size[1]

    filehead = (str(ImageFilePath).split(".png")[0]).split("/")[1]

    qr = Image.open(ImageFilePath)
    new_qr = qr.resize((round(qr.size[0] * x_scale), round(qr.size[1] * y_scale)))

    e_ticket = Image.new('RGB', background.size, (250,250,250))
    e_ticket.paste(background, (0,0))

    # if product == "MNight 2022 (5th March 2022)":
    #     offset = (int(round(((w - new_qr.size[0]) / 2), 0)) + 370, int(round(((h - new_qr.size[1]) / 2),0)) + 830)
    # else:
    #     offset = (int(round(((w - new_qr.size[0]) / 2), 0)), int(round(((h - new_qr.size[1]) / 2),0)) - 400)

    offset = (int(round(((w - new_qr.size[0]) / 2), 0)) + x_offset, int(round(((h - new_qr.size[1]) / 2))) + y_offset)
    e_ticket.paste(new_qr, offset, new_qr)
    e_ticket.save(f"e-tickets/{filehead}_eticket.pdf")