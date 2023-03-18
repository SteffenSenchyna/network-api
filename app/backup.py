import datetime
import os
import pytz
import requests
import json
from flask import Response
import napalm
from dotenv import load_dotenv
import boto3


def putS3(hostname, config):
    load_dotenv()
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_KEY"]
    )
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    formated_date = utc_now.strftime("%Y-%m-%dT%H-%M-%S")
    s3_client = session.resource("s3")
    s3_object = s3_client.Object(
        "network-conf", f'{hostname}/{formated_date}.txt')
    try:
        result = s3_object.put(Body=(config))
        return result
    except Exception as e:
        return e


def postBackup(request):
    print(request)
    ips = request.get_json()["ips"]
    print(ips)
    load_dotenv()
    driver = napalm.get_network_driver('ios')
    for i in ips:
        device = driver(hostname=i, username=os.environ["USER_NAME"], password=os.environ["PASSWORD"], optional_args={
                        'secret': os.environ["SECRET"]})
        try:
            device.open()
            hostname = device.get_facts()['hostname']
            config = device.get_config()['running']
            device.close()
            putS3(hostname, config)
        except Exception as e:
            print(f"Error: {e}")
            return Response(f"Error: {e}", status=400)

    return Response("Succesfully posted all backups to S3", status=201)
