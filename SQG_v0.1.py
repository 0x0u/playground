# Simple Query for GDSC
# Author: George Tsou

import requests
from urllib.parse import urlparse

print('Welcome to Simple Query for GDSC v0.1')
query = input('Please input an URL, IP or MD5 for query: ')

# query url on URLhaus
def url_UH():
    q = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data={'url': query})
    if q.json()['query_status'] == 'ok':
        p = q.json()["payloads"]
        p0 = p[0]
        pv = p0["virustotal"]
        return pv
    else:
        return None

# query host on URLhaus
def host_UH():
    if urlparse(query).hostname == None:
        return None
    else:
        host = urlparse(query).hostname
        q = requests.post('https://urlhaus-api.abuse.ch/v1/host/', data={'host': host})
        if q.json()['query_status'] == 'ok':
            p = q.json()["urlhaus_reference"]
            return p
        else:
            return None

# query ip on URLhaus
def ip_UH():
    q = requests.post('https://urlhaus-api.abuse.ch/v1/host/', data={'host': query})
    if q.json()['query_status'] == 'ok':
        p = q.json()["urlhaus_reference"]
        return p
    else:
        return None

# query MD5 on URLhaus
def md5_UH():
    q = requests.post('https://urlhaus-api.abuse.ch/v1/payload/', data={'md5_hash': query})
    if q.json()['query_status'] == 'ok':
        p = q.json()["virustotal"]
        return p
    else:
        return None

if url_UH() != None:
    print('\033[31mThe URL is potentially malicious!\033[0m')
    print('vt result:', url_UH()["result"], 'rf. link:', url_UH()["link"], sep='\n')

elif host_UH() != None:
    print('\033[31mThe host is potentially malicious!\033[0m')
    print('rf. link:', host_UH(), sep="\n")

else:
    print("No information yet.")

