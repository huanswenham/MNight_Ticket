import os

def folders_setup():
    for f in ["qrcodes", "etickets"]:
        if not os.path.isdir(f):
            print(f"folder {f} does not exist, creating a {f} folder...")
            os.mkdir(f)