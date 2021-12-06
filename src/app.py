from godaddypy import Client, Account
from os import environ
from pathlib import Path
import socket
from requests import get

my_acct = Account(api_key=environ["GODADDY_PUBLIC_KEY"], api_secret=environ["GODADDY_SECRET"])
client = Client(my_acct)

SUBDOMAINS = environ["GODADDY_SUBDOMAINS"].split(",")
MAINDOMAIN = environ["GODADDY_MAINDOMAIN"]
TESTDOMAIN = SUBDOMAINS[0] + "." + MAINDOMAIN

if len(SUBDOMAINS) == 0:
    raise Exception("No domains submitted in env variable GODADDY_DOMAINS")
else:
    print("checking for domains: " + str(SUBDOMAINS))

def getCurrentGodaddyIP():
    entries = client.get_records(MAINDOMAIN)
    for entry in entries:
        if entry["name"] in SUBDOMAINS:
            return entry["data"]
    # else
    return None

def getCurrentDNSIP():
    return socket.getaddrinfo(TESTDOMAIN, 443)[0][4][0]

def getCurrentServerIP():
    return get('https://api.ipify.org').text

def saveLastIP(ip):
    with open("persistent/lastip.txt", "w") as f:
        f.write(ip)
        
def updateIP(ip):
    for domain in SUBDOMAINS:
        domain += "." + MAINDOMAIN
        print("updating domain: " + domain)
        client.update_record_ip(ip, domain, "dynamic", "A")
    print("success! all domains updated to: " + ip)
    saveLastIP(ip)

# storage for current ip
my_file = Path("persistent/lastip.txt")
if my_file.is_file():
    with open("persistent/lastip.txt", "r") as f:
        LAST_IP = f.read()
else:
    LAST_IP = getCurrentGodaddyIP()
    saveLastIP(LAST_IP)
    


# get current server IP and check if is the same
server_ip = getCurrentServerIP()
if server_ip != LAST_IP:
    print("Server IP has changed for {}".format(TESTDOMAIN))
    print("Current server IP: {}".format(server_ip))
    print("Current godaddy IP: {}".format(LAST_IP))
else:
    print("all good")