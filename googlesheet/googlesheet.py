def write_new_entry(customer, sheet):
    """Writes a new customer data entry into Google Sheet.

    Args:
        customer (Customer): New customer data to be added.
        sheet (Worksheet): Google Sheet to edit.
    """
    name = str(customer.firstname) + " " + str(customer.surname)
    email = customer.email
    orNum = customer.ordernum
    quantity = int(customer.quantity)
    sheet.append_row([name, email, orNum, quantity, 0])
