import requests
import json
from flask import Response
from pprint import pprint
import csv
import io
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
 
# Opening JSON file and loading the data
# into the variable data

ipList = ["10.0.10.1"]
interfaceList = [["Interface Name", "Interface Description", "Interface Enabled", "IP Address", "Subnet Mask", "Duplex Mode", "Interface Speed"]]

for ip in ipList:
    url = f"https://{ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"
    headers = {
        "Accept" : "application/yang-data+json", 
        "Content-Type" : "application/yang-data+json", 
    }

    response = requests.get(url, headers=headers, auth=("admin", "cisco"), verify=False).json()
    # count = 0
    # intList = []
    # csvList = io.StringIO()
    # csv_writer = csv.writer(csvList)
    
    for i in response["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
        if i["admin-status"] == "if-state-up":
            interfaceList.append([i["name"], i["description"], i["admin-status"] , i["ipv4"], i["ipv4-subnet-mask"], i["ether-state"]["negotiated-duplex-mode"], i["ether-state"]["negotiated-port-speed"]])

print(interfaceList)
# Open a file for writing and create a CSV writer
with open('interfaces.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the data to the CSV file
    writer.writerows(interfaceList)


# for i in intList:
#     if count == 0:
#         header = i.keys()
#         csv_writer.writerow(header)
#         count += 1
#     csv_writer.writerow(i.values())

# csvlist = csvList.getvalue()
