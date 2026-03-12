import sys
from urllib.parse import urlsplit
import requests
import os
import pypatchergba
from pathlib import Path
import zipfile as zf
from patch_rom import patch_rom

##TODO:
# Add checksum checks
# IMPORTANT: Add .zip handling logic
# Add API handling of /any

def download_and_patch(link, path_folder, rom):
    if link == None:
        print("No link provided.")
        sys.exit(1)

    if rom == None:
        print("No vanilla SM64 ROM file provided.")
        sys.exit(1)

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
        sys.exit(1)

    try:
        rdl = requests.get(link_dl)
        open(path_folder + link.path, 'wb').write(rdl.content)
    except Exception as e:
        print("Could not download file {}".format(link_dl))
        print(e)
        sys.exit(1)

    #Check and handle .zip files
    if link.path[-3:] == "zip":
        print("INFO: A .zip file was downloaded from RHDC, contents will be listed and the bps patch will be applied.")
        try:    
            with zf.ZipFile(path_folder + link.path) as zip_dl:
                zip_dl.extractall(path_folder)
                for file in zip_dl.namelist():
                    print(file)
        except Exception as e:
            print("Error handling .zip file. " + str(e))
            sys.exit(1)
        try:
            for file in zip_dl.namelist():
                if file[-3:] == "bps":
                    print("BPS patch is " + file)
                    print(path_folder + "/" + file)
                    with open(path_folder + "/" + file, 'rb') as bps_patch: 
                        print("Opened bps patch")
                        #bps_path = path_folder + link.path
                        patch_rom(str(Path(rom).expanduser()), bps_patch.read(), path_folder , link)
        except Exception as e:
            print("Error patching file: " + str(e))
            sys.exit(1)
    else:
        try:
            print("Patching file...")
            with open(path_folder + link.path, 'rb').read() as bps_patch:
                patch_rom(str(Path(rom).expanduser()), bps_patch, path_folder, link)
        except Exception as e:
            print("Error patching file: " + str(e))
            sys.exit(1)

    print("Done! Patched ROM saved to: " + path_folder + link.path[:-4] + ".z64")