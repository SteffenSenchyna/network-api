import requests
import json
from flask import Response
from pprint import pprint
import csv
import io
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def get_int(request):
    #Grab request
    req_json = request.get_json()
    interfaceList = [["Interface Name", "Interface Description", "Interface Enabled", "IP Address", "Subnet Mask", "Duplex Mode", "Interface Speed"]]
    ipList = req_json["ips"]
    #Deploy commands to switch
    for ip in ipList:
        url = f"https://{ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"
        headers = {
            "Accept" : "application/yang-data+json", 
            "Content-Type" : "application/yang-data+json", 
        }

        response = requests.get(url, headers=headers, auth=("admin", "cisco"), verify=False).json()
        #Initializing cvs writer to fill with repsonse 
        csvList = io.StringIO()
        csv_writer = csv.writer(csvList)
        csv_writer.writerows(interfaceList)
        #Only Grabbing up interfaces
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
    #Grab request
    req_json = request.get_json()
    ipList = req_json["ips"]
    payload = req_json["commands"]
    print(payload)
    try:
        for ip in ipList:
            url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces"
            headers = {
                "Accept" : "application/yang-data+json", 
                "Content-Type" : "application/yang-data+json", 
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload), auth=("admin", "cisco"), verify=False)
            #Showing if succesful
            print(ip)
            print(response.text)   
            print(response.status_code)
        return Response("Succesfully added all the users", status=201)
    #Error Handling
    except Exception as e:
        print(e)
        return Response("Error", status=400)



    

