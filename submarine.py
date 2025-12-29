#!/usr/bin/env python3
#   Submarine           v1.3
#   Author  jts.gg/submarine 

import sys
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

WORDLIST_URL  = "https://wordlist.jts.gg/subdomains"
WORDLIST      = requests.get(WORDLIST_URL, timeout=5).text
WORDS         = [sub.strip() for sub in WORDLIST.splitlines() if sub.strip()]
DOMAIN        = sys.argv[1]
IP            = ""
WORKERS       = 1000

def subdomain_check(subdomain):
    global IP
    try:
        IP = str(socket.gethostbyname(f"{subdomain}.{DOMAIN}"))
        return True
    except Exception:
        return False

def main():    
    with ThreadPoolExecutor(max_workers=WORKERS) as exe:
        futures = {exe.submit(subdomain_check, subdomain): subdomain for subdomain in WORDS}
        
        for future in as_completed(futures):
            subdomain = futures[future]
            if future.result():
                output_buffer = (len(DOMAIN) + 24)
                print((f"{subdomain}.{DOMAIN}" + " " * output_buffer)[:output_buffer], IP)
        return
                
main()
