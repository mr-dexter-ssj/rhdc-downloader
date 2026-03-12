import pypatchergba
import sys

def patch_rom(rom, bps_patch, path_folder, link):   
    try:
        patched_rom = pypatchergba.apply_patch(rom, bps_patch)
        open(path_folder + link.path[:-4] + ".z64", 'wb').write(patched_rom)
    except Exception as e:
        print("Error: " + str(e))
        sys.exit(1)