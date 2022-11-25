import os
import csv
from netmiko import ConnectHandler

def createReport(request):    
    username = os.environ['username']
    password = os.environ['password']
    secret = os.environ['secret']
    req_json = request.get_json()
    ipAddress = req_json["ipAdddress"]
    
    device = {
        "device_type": "cisco_ios",
        "ip": ipAddress,
        "username": username,
        "password": password,
        "secret": secret
    }


    #Connecting to the device and stoing the output 
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        output = net_connect.send_command("show interface summary", use_textfsm=True)
        #storing output as dictionary with the textfsm command 
        output = output[0]
        #storing the needed variables 
        intName = output["Interface Name"]
        port = output["port"]
        vlanID = output["Vlan Id"]
        portIP = output["IP Address"]
        portType = output["Type"]   
    #Error Handling
    except Exception as e:
        print(e)
    #Stating headers for the csv file
    headers = ["intName", "port", "vlanID", "portIP", "portType"]
    #Writing the file to csv 
    with open ("file.csv", "w") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerow({"intName": intName, "port": port, "vlanID": vlanID, "portIP": portIP, "portType": portType})
    