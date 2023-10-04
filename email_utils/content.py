import re
import json
import os


def compile_email_content(firstname, surname, quantity):
    replacements = _compile_replacements(firstname, surname, quantity)
    email = _read_content(replacements)
    email = _replace_title_img(email)
    return email


def _read_content(replacements):
    content = open("email_templates/content.txt").read()
    content = re.sub(r"[\n\t]*", "", content)
    email = open("email_templates/email.html").read()
    new_email = email.replace("{CONTENT}", content)

    for tag in replacements:
        new_email = new_email.replace("{" + tag + "}", replacements[tag])
    return new_email


def _replace_title_img(email):
    title_img_url = os.getenv("EMAIL_TITLE_IMG", default="#")
    return email.replace("{EMAIL_TITLE_IMG}", title_img_url)


def _compile_replacements(firstname, surname, quantity):
    replacements = {}
    with open("email_templates/values.json") as replacements_json:
        replacements = json.load(replacements_json)
    replacements["name"] = firstname + " " + surname
    replacements["quantity"] = str(quantity)
    return replacements