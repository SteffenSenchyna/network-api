import os
from pprint import pprint
import subprocess
import threading
import json
from dotenv import load_dotenv
from flask import Response
import requests


def getScan(request):
    load_dotenv()
    env = os.environ["ENV"]
    if env == "local":
        url = "http://0.0.0.0:8000/api/dcim/devices/"
    else:
        url = "http://netbox-docker-netbox-1:8080/api/dcim/devices/"
    threads = []
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': os.environ["NETBOXTOKEN"]
    }
    if os.environ["ENV"] == "local":
        response = requests.get(url, headers=headers).json()
        response = response["results"]
        # for i in response:
        #     pprint(i["primary_ip4"]["address"])

    def ping(ip, host):
        result = subprocess.run(
            ['ping', '-c', '1', ip], stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            host["ping_status"] = "up"
        else:
            host["ping_status"] = "down"

    try:
        for i in response:
            t = threading.Thread(target=ping, args=(
                i["primary_ip4"]["address"], i))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        totalDevicesMain = 0
        totalDevicesRemote = 0
        downDevicesMain = 0
        upDevicesMain = 0
        downDevicesRemote = 0
        upDevicesRemote = 0
        devicesMain = []
        devicesRemote = []
        for i in response:
            if i["site"]["slug"] == "hmc-coporate-headquaters":
                devicesMain.append(i)
                totalDevicesMain += 1
                if i["ping_status"] == "up":
                    upDevicesMain += 1
                else:
                    downDevicesMain += 1
            else:
                totalDevicesRemote += 1
                devicesRemote.append(i)
                if i["ping_status"] == "up":
                    upDevicesRemote += 1
                else:
                    downDevicesRemote += 1

        webResponse = {
            "devicesRemote": devicesRemote,
            "devicesMain": devicesMain,
            "downDevicesMain": downDevicesRemote,
            "upDevicesMain": upDevicesRemote,
            "downDevicesMain": downDevicesMain,
            "downDevicesRemote": downDevicesRemote,
            "upDevicesRemote": upDevicesMain,
            "upDevicesMain": upDevicesMain,
            "totalDevicesMain": totalDevicesMain,
            "totalDevicesRemote": totalDevicesRemote
        }
        return Response(json.dumps(webResponse), status=200)
    except Exception as e:
        print(e)
        return Response(e, status=400)
