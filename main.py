import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from argparse import ArgumentParser
import os
from dl import download_and_patch
from pathlib import Path

#-----------CLI App definition-----------

default_dl_folder = str(Path("~" + "/Downloads").expanduser())
print("Default download folder: " + default_dl_folder)

mainParser = ArgumentParser(prog="rhdc-downloader", description="A tool to download Super Mario 64 romhacks from romhacking.com using the \"Play now!\" button without depending on Parallel Launcher.")
mainParser.add_argument('-l', '--link')
mainParser.add_argument('-p', '--path', default=default_dl_folder) 
mainParser.add_argument('-r', '--rom', help='Path to your own vanilla SM64 ROM file')

#Args stored here:
args = mainParser.parse_args()
##################

print(args.link)
print(args.path)
print(args.rom)

download_and_patch(args.link, args.path, args.rom)

sys.exit(0)

