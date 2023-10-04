import os
import json
import gspread
from google.oauth2.service_account import Credentials


ENV_VAR_NULL_CHECK_LIST = [
    "OLD_CSV_FILE_PATH", 
    "NEW_CSV_FILE_PATH", 
    "SENDER_EMAIL", 
    "SENDER_PASSWORD",
    "QRCODE_PAGE_BACKGROUND_FILE_PATH",
    "QRCODE_HAS_TRANSPARENT_BACKGROUND",
    "QRCODE_BACKGROUND_RGBA_COLOR",
    "GOOGLE_SHEET_NAME",
    "EMAIL_SUBJECT",
    "EMAIL_TITLE_IMG",
    "EMAIL_CONTENT",
    "EMAIL_VALUES"
]

ENV_VAR_CSV_FILE_PATH_CHECK_LIST = [
    "OLD_CSV_FILE_PATH", 
    "NEW_CSV_FILE_PATH",
]

ENV_VAR_IMG_FILE_PATH_CHECK_LIST = [
    "QRCODE_PAGE_BACKGROUND_FILE_PATH"
]

ENV_VAR_TXT_FILE_PATH_CHECK_LIST = [
    "EMAIL_CONTENT"
]

ENV_VAR_JSON_FILE_PATH_CHECK_LIST = [
    "EMAIL_VALUES"
]

GOOGLE_SCOPE = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]



def valid_env():
    """Checks if all env variables are valid.

    Returns:
        boolean: Validity of env variables.
    """
    
    for name, value in os.environ.items():
        if not value and name in ENV_VAR_NULL_CHECK_LIST:
            print(f"value for {name} not provided in .env file, please provide a value for this field.")
            return False
    
    if not _valid_color_env(): return False
    elif not _valid_qr_has_trans_env(): return False
    elif not _valid_qr_scale_env(): return False
    elif not _valid_qr_offset_env(): return False
    elif not _valid_img_files_env(): return False
    elif not _valid_txt_files_env(): return False
    elif not _valid_json_files_env(): return False

    return True


def _valid_color_env():
    color = os.getenv("QRCODE_BACKGROUND_RGBA_COLOR", default=None)
    rgba_ls = color.split(" ")
    
    if not len(rgba_ls) == 4:
        print("Invalid rgba value for QRCODE_BACKGROUND_RGBA_COLOR provided in .env file, please use the format \'\{R value\} \{G value\} \{B value\} \{Alpha value\}\'")
        return False

    for value in rgba_ls:
        if not value.isdigit() or 0 > int(value) or int(value) > 255:
            print("Invalid RGBA values for QRCODE_BACKGROUND_RGBA_COLOR provided in .env file, please make sure each RGBA value is between 0 and 255")
            return False
    
    return True


def _valid_qr_has_trans_env():
    has_trans_bg = os.getenv("QRCODE_HAS_TRANSPARENT_BACKGROUND", default=None)
    if not (has_trans_bg == "True" or has_trans_bg == "False"):
        print(f"value for QRCODE_HAS_TRANSPARENT_BACKGROUND is either empty or not a boolean (True / False) in .env file, please provide a valid boolean.")
        return False
    return True


def _valid_qr_scale_env():
    for field in ["QRCODE_X_SIZE_SCALE", "QRCODE_Y_SIZE_SCALE"]:
        scale = os.getenv(field, default=None)
        try:
            float(scale)
        except ValueError:
            print(f"value for {field} is either empty or not a number in .env file, please provide a valid number.")
            return False
    return True


def _valid_qr_offset_env():
    for field in ["QRCODE_X_OFFSET", "QRCODE_Y_OFFSET"]:
        offset = os.getenv(field, default=None)
        try:
            int(offset)
        except ValueError:
            print(f"value for {field} is either empty or not a integer in .env file, please provide a valid integer.")
            return False
    return True


def _valid_img_files_env():
    for field in ENV_VAR_CSV_FILE_PATH_CHECK_LIST:
        csv_fp = os.getenv(field, default=None)
        if not csv_fp.split(".")[-1] == "csv":
            print(f"value for {field} is not a valid csv file path, please provide a valid csv file path.")
            return False
        elif not os.path.isfile(csv_fp):
            print(f"csv file provided for {field} is not found, please provide a valid csv file path.")
            return False
    
    for field in ENV_VAR_IMG_FILE_PATH_CHECK_LIST:
        img_fp = os.getenv(field, default=None)
        if img_fp.split(".")[-1] not in ["jgp", "png", "jpeg"]:
            print(f"value for {field} is not a valid image file path, please provide a valid image file path.")
            return False
        elif not os.path.isfile(img_fp):
            print(f"image file provided for {field} is not found, please provide a valid image file path.")
            return False
    return True


def _valid_txt_files_env():
    for field in ENV_VAR_TXT_FILE_PATH_CHECK_LIST:
        txt_fp = os.getenv(field, default=None)
        if not txt_fp.split(".")[-1] == "txt":
            print(f"value for {field} is not a valid txt file path, please provide a valid txt file path.")
            return False
        elif not os.path.isfile(txt_fp):
            print(f"txt file provided for {field} is not found, please provide a valid txt file path.")
            return False
    return True


def _valid_json_files_env():
    for field in ENV_VAR_JSON_FILE_PATH_CHECK_LIST:
        json_fp = os.getenv(field, default=None)
        if not json_fp.split(".")[-1] == "json":
            print(f"value for {field} is not a valid json file path, please provide a valid json file path.")
            return False
        elif not os.path.isfile(json_fp):
            print(f"json file provided for {field} is not found, please provide a valid json file path.")
            return False
    return True



def google_sheet_init():
  """Initialise a Google Sheet by accessing Google account defined in creds.json.

  Returns:
      Worksheet: Google Sheet to be read and written into.
  """

  try:
      keyfile_dict = {}
      with open("creds.json") as creds_json:
          keyfile_dict = json.load(creds_json)
      creds = Credentials.from_service_account_info(keyfile_dict, scopes=GOOGLE_SCOPE)

      client = gspread.authorize(creds)

      return client.open(os.getenv("GOOGLE_SHEET_NAME", default="")).sheet1
  except:
      print(f"Error initializing Google Sheet connection, please check your creds.json and the value for GOOGLE_SHEET_NAME in .env file.")
      return None