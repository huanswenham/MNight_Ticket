import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# define keyfile_dict here

creds = Credentials.from_service_account_info(keyfile_dict, scopes=scope)

client = gspread.authorize(creds)

sheet = client.open("tickettesting").sheet1


def transfer(customers):
  print("Reach transfer")

  for customer in customers:
      name = str(customer.firstname) + " " + str(customer.surname)
      email = customer.email
      orNum = customer.ordernum
      quantity = int(customer.quantity)
      sheet.append_row([name, email, orNum, quantity, 0])

# transfer("ticlet-qr-2.csv")