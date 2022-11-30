import requests
import json
from flask import Response
from pprint import pprint
import csv
import io

def get_int(request):
    req_json = request.get_json()
    pprint(req_json)

    url = "https://10.0.10.5/restconf/data/Cisco-IOS-XE-native:native/interface"
    headers = {
        "Accept" : "application/yang-data+json", 
        "Content-Type" : "application/yang-data+json", 
    }

    response = requests.get(url, headers=headers, auth=("admin", "cisco"), verify=False).json()
    count = 0
    intList = []
    csvList = io.StringIO()
    csv_writer = csv.writer(csvList)

    for i in response["Cisco-IOS-XE-native:interface"]["GigabitEthernet"]:
        if "ip" in i:
            intList.append(i)

    for i in intList:
        if count == 0:
            header = i.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(i.values())

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
        return Response("Successfully added interface", status=response.status_code)
    else:
        return Response(response.text, status=response.status_code)


    

