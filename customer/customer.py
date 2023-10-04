class Customer:
    def __init__(self, ordernum, firstname, surname, name, email, qrpath, pdfpath, product, quantity):
        self.ordernum = ordernum
        self.firstname = firstname
        self.surname = surname
        self.name = name
        self.email = email
        self.qrpath = qrpath
        self.pdfpath = pdfpath
        self.product = product
        self.quantity = quantity