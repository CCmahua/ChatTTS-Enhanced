import os
import sys
import platform



def open_folder(folder_path):
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    folder_path=os.path.join(script_dir, folder_path)
    if platform.system() == "Windows":
        os.startfile(folder_path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {folder_path}")
    else:  # Linux and others
        os.system(f"xdg-open {folder_path}")
    return "Folder opened."