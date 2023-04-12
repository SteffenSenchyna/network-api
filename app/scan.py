import os
from pprint import pprint
import subprocess
import threading
import json
from dotenv import load_dotenv
from flask import Response
import requests


def getScan():
    load_dotenv()
    NETBOXURL = os.environ["NETBOXURL"]
    NETBOXTOKEN = os.environ["NETBOXTOKEN"]
    url = f"http://{NETBOXURL}/api/dcim/devices/"
    threads = []
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Token {NETBOXTOKEN}"
    }
    try:
        response = requests.get(url, headers=headers).json()
        response = response["results"]
    except Exception as e:
        print(e)
        return Response(str(e), status=400)
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
            ip = i["primary_ip4"]["address"].split("/")
            t = threading.Thread(target=ping, args=(
                ip[0], i))
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
                totalDevicesMain += 1
                devicesMain.append(i)
            else:
                totalDevicesRemote += 1
                devicesRemote.append(i)

        for i in devicesMain:
            if i["ping_status"] == "up":
                upDevicesMain += 1
            else:
                downDevicesMain += 1

        for i in devicesRemote:
            if i["ping_status"] == "up":
                upDevicesRemote += 1
            else:
                downDevicesRemote += 1

        webResponse = {
            "devicesRemote": devicesRemote,
            "devicesMain": devicesMain,
            "downDevicesMain": downDevicesMain,
            "upDevicesMain": upDevicesMain,
            "downDevicesMain": downDevicesMain,
            "downDevicesRemote": downDevicesRemote,
            "upDevicesRemote": upDevicesRemote,
            "upDevicesMain": upDevicesMain,
            "totalDevicesMain": totalDevicesMain,
            "totalDevicesRemote": totalDevicesRemote
        }
        return Response(json.dumps(webResponse), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(str(e), status=400)
