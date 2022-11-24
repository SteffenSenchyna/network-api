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
        outputV = net_connect.send_command("show int brief", use_textfsm=True)
        #storing output as dictionary with the textfsm command 
        outputV = outputV[0]
        #storing the needed variables 
        Hostname = outputV["hostname"]
        MAC = outputV["mac"]
        Hardware = outputV["hardware"][0]
        SN = outputV["serial"][0]
        OS = outputV["rommon"]
        OSV = outputV["version"]
        uptime = outputV["uptime"]   
    #Error Handling
    except Exception as e:
        print(e)
    #Stating headers for the csv file
    headers = ["Hostname", "MAC", "Hardware", "SN", "OS", "OSV", "uptime"]
    #Writing the file to csv 
    with open ("file.csv", "w") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerow({"Hostname": Hostname, "MAC": MAC, "Hardware": Hardware, "SN": SN, "OS": OS, "OSV": OSV, "uptime": uptime})