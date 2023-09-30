def transfer(customers, sheet):
  for customer in customers:
      name = str(customer.firstname) + " " + str(customer.surname)
      email = customer.email
      orNum = customer.ordernum
      quantity = int(customer.quantity)
      sheet.append_row([name, email, orNum, quantity, 0])