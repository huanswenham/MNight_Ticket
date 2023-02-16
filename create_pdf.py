from PIL import Image

COLOR = (252,233,232)
ADDITIANAL_IMAGES = []
BACKGROUND_PATH = ""
# QRCODE_TITLE = "_welcome"


def Reformat_QR(ImageFilePath, product):
    qrcode = Image.open(ImageFilePath, 'r')
    qr_rgba = qrcode.convert("RGBA")
    datas = qr_rgba.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    qr_rgba.putdata(newData)
    qr_rgba.save(ImageFilePath, "PNG")
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
    # if product == "MNight 2022 (5th March 2022)":
    #     background = Image.open("eticket_background_5th.png")
    #     w = background.size[0]
    #     h = background.size[1]
    # else:
    #     background = Image.open("eticket_background_6th.png")
    #     w = background.size[0]
    #     h = background.size[1]
    background = Image.open(BACKGROUND_PATH)
    w = background.size[0]
    h = background.size[1]

    filehead = (ImageFilePath.split(".")[0]).split("/")[1]

    qr = Image.open(ImageFilePath)
    new_qr = qr.resize((round(qr.size[0]), round(qr.size[1])))

    e_ticket = Image.new('RGB', background.size, (250,250,250))
    e_ticket.paste(background, (0,0))
    # if product == "MNight 2022 (5th March 2022)":
    #     offset = (int(round(((w - new_qr.size[0]) / 2), 0)) + 370, int(round(((h - new_qr.size[1]) / 2),0)) + 830)
    # else:
    #     offset = (int(round(((w - new_qr.size[0]) / 2), 0)), int(round(((h - new_qr.size[1]) / 2),0)) - 400)
    offset = (int(round(((w - new_qr.size[0]) / 2), 0)) + 170, int(round(((h - new_qr.size[1]) / 2))) + 400)
    e_ticket.paste(new_qr, offset, new_qr)
    e_ticket.save(f"e-tickets/{filehead}_eticket.pdf")