# Network-API
This is a RESTful API built with Flask and designed to manage/monitor on-premise network devices. The API exposes three endpoints:  
* /health: A health check endpoint for Kubernetes readiness probes at /health.
* /network/backup: a POST endpoint to initiate a backup of the network configuration
* /network/scan: a GET endpoint to trigger a network scan. 

The API is built with a Dockerfile, and a Jenkins CI pipeline manages the build process; the microservice is then deployed with Helm charts through a CD pipeline using ArgoCD. The API is part of a larger project, which includes several microservices and other components that collectively provide tools to manage on-premise networking devices. The view the cluster architecture and the CI/CD pipeline for deployment, refer to the [Cluster Manifest Repository](https://github.com/SteffenSenchyna/cluster-chart).

## Prerequisites 
* Python 3.7 or later
* An AWS account with access to S3
* Network devices compatible with the Napalm library

## Getting Started
To run this application, follow these steps:
* Clone this repository
* Install the required packages using `pip install -r requirements.txt`
* Run the application using `python app.py`
* The application will be hosted at `http://localhost:8081`

## API Endpoints
This application has the following API endpoints:

### POST /network/backup
This endpoint performs network backups for multiple devices and stores them in an AWS S3 bucket. It uses Napalm, a Python library that makes it easy to automate the configuration and management of network devices. This code is written for IOS network devices. However, the code can be easily modified to support other network devices.  
#### Request Body
The request body should contain the following:
```
{
    "ips": [
        "192.0.2.1",
        "192.0.2.2",
        "192.0.2.3"
    ]
}
```

### GET /network/scan
This endpoint is a network scanner that performs an ICMP ping sweep on devices in a network to determine their availability status. It pulls the device list to ping from the NetBox library. It also filters devices based on their location (Main or Remote) and returns the results in a JSON format.
#### Response
If the scan is successful, the response will be:
```
{
  "devicesRemote": <A list of devices located in the main site>,
  "devicesMain": <A list of devices located in remote sites>,
  "downDevicesMain": <The number of devices located in the main site that are currently down>,
  "upDevicesMain": <The number of devices located in the main site that are currently up>,
  "downDevicesMain": <The number of devices located in remote sites that are currently down>,
  "downDevicesRemote": <The number of devices located in remote sites that are currently up>,
  "totalDevicesMain": <The total number of devices located in the main site>,
  "totalDevicesRemote": <The total number of devices located in the remote site>
}
```
## Environmental Variables
Create a .env file in the root directory of the project and set the following environment variables:
```
AWS_ACCESS_KEY=<aws_access_key>
AWS_SECRET_KEY=<aws_secret_key>
NETBOXTOKEN=<netbox_token>
NETBOXURL=<netbox_url>
USERNAME=<network_device_username>
PASSWORD=<network_device_password>
SECRET=<network_device_secret>
```
