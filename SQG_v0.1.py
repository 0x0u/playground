# Simple Query for GDSC
# Author: George Tsou

import requests
import base64
from urllib.parse import urlparse

vt_apikey = 'your vt api key'

print('Welcome to Simple Query for GDSC v0.1')
query = input('Please input an URL, IP or hash for query: ')

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

# query domain on URLhaus
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

# query URL on vt
def url_vt():
    url_id = base64.urlsafe_b64encode(query.encode()).decode().strip("=")
    url = 'https://www.virustotal.com/api/v3/urls/' + url_id
    q = requests.get(url, headers={'x-apikey': vt_apikey})
    p = q.json()
    d = list(p.keys())[0]
    if d != 'error':
        pa = p['data']['attributes']['last_analysis_stats']
        return pa
    else:
        return None

# query hash on vt
def hash_vt():
    url = 'https://www.virustotal.com/api/v3/files/' + query
    q = requests.get(url, headers={'x-apikey': vt_apikey})
    p = q.json()
    d = list(p.keys())[0]
    if d != 'error':
        pa = p['data']['attributes']['last_analysis_stats']
        return pa
    else:
        return None

if url_UH() != None:
    print('\033[31mThe URL is potentially malicious!\033[0m')
    print('vt result:', url_UH()["result"], 'rf. link:', url_UH()["link"], sep='\n')

elif host_UH() != None:
    print('\033[31mThe host is potentially malicious!\033[0m')
    print('rf. link:', host_UH(), sep="\n")

elif url_vt() != None:
    if url_vt()['malicious'] > 0 or url_vt()['suspicious'] > 0:
        print('\033[31mThe url is potentially malicious!\033[0m')
        print('malicious:',url_vt()['malicious'], ' suspicious:', url_vt()['suspicious'])
    else:
        print("No suspicious information yet.")

elif hash_vt() != None:
    if hash_vt()['malicious'] > 0 or hash_vt()['suspicious'] > 0:
        print('\033[31mThe file is potentially malicious!\033[0m')
        print('malicious:',hash_vt()['malicious'], ' suspicious:', hash_vt()['suspicious'])
    else:
        print("No suspicious information yet.")

else:
    print("No suspicious information yet.")