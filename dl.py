from urllib.parse import urlsplit
import requests
import os
import pypatchergba
from pathlib import Path

##TODO:
# Add checksum checks
# IMPORTANT: Add .zip handling logic
# Add API handling of /any

def download_and_patch(link, path_folder, rom):
    if link == None:
        print("No link provided.")
        exit(1)

    if rom == None:
        print("No vanilla SM64 ROM file provided.")
        exit(1)

    url_rhdc = "https://api.romhacking.com/game/"
    link = urlsplit(link)
    print(link)
    print("Hack name: " + link.netloc)
    print("Hack version/file: " + link.path)

    link_dl = url_rhdc + link.netloc + link.path

    print("Downloading file from: " + link_dl)
    print("To: " + str(Path(path_folder).expanduser()))

    if os.path.exists(path_folder) == False:
        print("The given download path does not exist. Please input a valid path.")
        exit(1)

    try:
        rdl = requests.get(link_dl)
        open(path_folder + link.path, 'wb').write(rdl.content)
    except Exception as e:
        print("Could not download file {}".format(link_dl))
        print(e)
        exit(1)

    print("Patching file...")
    bps_patch = open(path_folder + link.path, 'rb').read()

    try:
        patched_rom = pypatchergba.apply_patch(str(Path(rom).expanduser()), bps_patch)
        open(path_folder + link.path[:-4] + ".z64", 'wb').write(patched_rom)
    except Exception as e:
        print("Error: " + str(e))
        exit(1)

    print("Done! Patched ROM saved to: " + path_folder + link.path[:-4] + ".z64")