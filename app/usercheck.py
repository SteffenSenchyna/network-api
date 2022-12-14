import requests
import json
from flask import Response
from pprint import pprint
import csv
import io
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



ipList = ["10.0.10.1", "10.0.10.2", "10.0.10.3", "10.0.10.4", "10.0.10.5"]
userList = []
for ip in ipList:
    url = f"https://{ip}/restconf/data/Cisco-IOS-XE-native:native/username"
    headers = {
        "Accept" : "application/yang-data+json", 
        "Content-Type" : "application/yang-data+json", 
    }
    response = requests.get(url, headers=headers, auth=("admin", "cisco"), verify=False).json()
    print(ip)
    pprint(response)