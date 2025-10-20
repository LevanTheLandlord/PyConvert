import winreg
import sys

def uninstall_context_menu():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\PyConvert\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\PyConvert")
        return True
    except FileNotFoundError:
        return True
    except Exception:
        return False

if __name__ == "__main__":
    uninstall_context_menu()