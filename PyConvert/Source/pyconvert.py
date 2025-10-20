import os
import sys
import winreg
from pathlib import Path

def install_context_menu():
    try:
        exe_path = os.path.abspath(sys.argv[0])
        
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell", 0, winreg.KEY_WRITE) as key:
            with winreg.CreateKeyEx(key, "PyConvert", 0, winreg.KEY_WRITE) as pyconvert_key:
                winreg.SetValueEx(pyconvert_key, "Icon", 0, winreg.REG_SZ, exe_path)
                winreg.SetValueEx(pyconvert_key, "", 0, winreg.REG_SZ, "Convert to Python")
                
                with winreg.CreateKeyEx(pyconvert_key, "command", 0, winreg.KEY_WRITE) as command_key:
                    winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, f'"{exe_path}" "%1"')
        return True
    except Exception:
        return False

def uninstall_context_menu():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\PyConvert\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\PyConvert")
        return True
    except FileNotFoundError:
        return True
    except Exception:
        return False

def convert_file(file_path):
    try:
        path = Path(file_path)
        if not path.exists():
            return False
        
        new_path = path.with_suffix('.py')
        if new_path.exists():
            counter = 1
            while True:
                newer_path = path.with_name(f"{path.stem}_{counter}.py")
                if not newer_path.exists():
                    new_path = newer_path
                    break
                counter += 1
        
        path.rename(new_path)
        return True
    except Exception:
        return False

def main():
    if len(sys.argv) == 1:
        install_context_menu()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--uninstall":
            uninstall_context_menu()
        else:
            convert_file(sys.argv[1])

if __name__ == "__main__":
    main()