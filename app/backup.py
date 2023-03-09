import os
import requests
import json
from flask import Response
import napalm
from dotenv import load_dotenv

load_dotenv()

def getBackup(ip):
    driver = napalm.get_network_driver('ios')
    device = driver(hostname=ip, username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"), optional_args={'secret': os.getenv("SECRET")})
    print(device)
    try:
        device.open()
        config = device.get_config()
        device.close()
        return config['running']

    except Exception as e:
        print(f"Error: {e}")
        return None


getBackup("10.0.5.21")


