def write_new_data(customers, sheet):
  """Writes new customers data into Google Sheet.

  Args:
      customers (List[Customer]): New customers.
      sheet (Worksheet): Google Sheet to edit.
  """
  for c in customers:
      name = str(c.firstname) + " " + str(c.surname)
      email = c.email
      orNum = c.ordernum
      quantity = int(c.quantity)
      sheet.append_row([name, email, orNum, quantity, 0])