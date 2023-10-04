def write_new_data(customers, sheet):
  for c in customers:
      name = str(c.firstname) + " " + str(c.surname)
      email = c.email
      orNum = c.ordernum
      quantity = int(c.quantity)
      sheet.append_row([name, email, orNum, quantity, 0])