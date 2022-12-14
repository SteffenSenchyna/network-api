import requests
import json
from flask import Response
from pprint import pprint
import csv
import io
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



def get_int(request):
    req_json = request.get_json()
    interfaceList = [["Interface Name", "Interface Description", "Interface Enabled", "IP Address", "Subnet Mask", "Duplex Mode", "Interface Speed"]]
    ipList = req_json["ips"]
    for ip in ipList:
        url = f"https://{ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"
        headers = {
            "Accept" : "application/yang-data+json", 
            "Content-Type" : "application/yang-data+json", 
        }

        response = requests.get(url, headers=headers, auth=("admin", "cisco"), verify=False).json()
        # count = 0
        # intList = []
        csvList = io.StringIO()
        csv_writer = csv.writer(csvList)
        csv_writer.writerows(interfaceList)
        
        for i in response["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
            if i["admin-status"] == "if-state-up":
                interfaceList.append([i["name"], i["description"], i["admin-status"] , i["ipv4"], i["ipv4-subnet-mask"], i["ether-state"]["negotiated-duplex-mode"], i["ether-state"]["negotiated-port-speed"]])

    print(interfaceList)
    # Open a file for writing and create a CSV writer
    with open('interfaces.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the data to the CSV file
        writer.writerows(interfaceList)

    csvlist = csvList.getvalue()
    return Response(csvlist, status=200, mimetype="application/csv")

def create_int(request):
    payload = request.get_json()

    url = "https://10.0.10.5/restconf/data/ietf-interfaces:interfaces"
    headers = {
        "Accept" : "application/yang-data+json", 
        "Content-Type" : "application/yang-data+json", 
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=headers, data=json.dumps(payload), auth=("admin", "cisco"), verify=False)

    if (response.status_code == 201):
        print("Successfully added interface")
        return Response(response.text, status=response.status_code)
    else:
        return Response(response.text, status=response.status_code)


    

