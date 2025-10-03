import os
import rarfile

rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
RAR_PATH = r"C:\Users\LENOVO\Desktop\ERASMUS.rar"
PW_FILE  = r"C:\Users\LENOVO\SecLists\Passwords\Common-Credentials\100k-most-used-passwords-NCSC.txt"

def extract_rar(rar_path: str, password: str, dest_dir: str = None):
    if dest_dir is None:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        dest_dir = os.path.join(desktop, os.path.splitext(os.path.basename(rar_path))[0] + "_extracted")
    os.makedirs(dest_dir, exist_ok=True)

    try:
        rf = rarfile.RarFile(rar_path)
        rf.extractall(path=dest_dir, pwd=password)
        rf.close()
        print(f"[+] Başarılı: '{rar_path}' klasöre çıkarıldı -> {dest_dir}")
        return True
    except rarfile.RarWrongPassword:
        return False
    except rarfile.BadRarFile:
        return False
    except FileNotFoundError:
        print("[!] Hata: 'unrar' / 'unar' yüklü değil veya PATH'te değil.")
        return False
    except Exception as e:
        print(f"[!] Beklenmeyen hata: {e}")
        return False

def extract_rar_from_txt(rar_path: str, pw_file: str):
    pw_file = os.path.normpath(pw_file.strip().strip('"').strip("'"))
    if not os.path.isfile(pw_file):
        print(f"[!] Hata: Parola dosyası bulunamadı -> {pw_file}")
        return

    with open(pw_file, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip().strip('"').strip("'") for line in f.readlines() if line.strip()]

    if not passwords:
        print("[!] Hata: Parola dosyası boş.")
        return

    for i, pw in enumerate(passwords, start=1):
        display_pw = pw if len(pw) <= 30 else pw[:27] + "..."
        if extract_rar(rar_path, pw):
            print(f"[+] Parola bulundu: '{pw}'")
            return

    print("[!] Tüm parolalar denendi, doğru parola bulunamadı.")

if __name__ == "__main__":
    extract_rar_from_txt(RAR_PATH, PW_FILE)
