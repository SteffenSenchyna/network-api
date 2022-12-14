import requests
import json
from flask import Response
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def create_user(request):
    #Grab request
    req_json = request.get_json()
    ipList = req_json["ips"]
    payload = req_json["commands"]
    #Deploy commands to switch
    try:
        for ip in ipList:
            url = f"https://{ip}/restconf/data/Cisco-IOS-XE-native:native"
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

