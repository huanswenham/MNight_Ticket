def read_mail(firstname, surname, quantity, product):
    text = open("email_templates/email.html").read()
    new_text1 = text.replace("{name}", firstname + " " + surname)
    new_text2 = new_text1.replace("{quantity}", str(quantity))
    new_text3 = new_text2.replace("{date}", "6th of October 2022")
    # if product == "MNight 2022 (5th March 2022)":
    #     new_text3 = new_text2.replace("{date}", "5th of March 2022")
    # else:
    #     new_text3 = new_text2.replace("{date}", "6th of March 2022")
    return new_text3