#!/usr/bin/env python3
"""Program to audit the store network and look for APs that are offline,
based on the S/N of the device. This way it will ignore other devices in the network"""

#imports
import re
import requests

#Import the CRED module from a separate directory ****Only Usable when I run this script locally
import cred

#This pulls the information based on s/ns that start with these.
REGEX = re.compile('Q2PD')
REGEX1 = re.compile('Q2HD')

#custom variables for the program imported from the cred.py file located in the same directory
ORGANIZATION = cred.organization
KEY = cred.key

#Main URL for the Meraki Platform
DASHBOARD = "https://dashboard.meraki.com"
#api token and other data that needs to be uploaded in the header
HEADERS = {'X-Cisco-Meraki-API-Key': (KEY), 'Content-Type': 'application/json'}

#Pull back all of the network IDs:
GET_NETWORK_URL = DASHBOARD + '/api/v0/organizations/%s/networks' % ORGANIZATION
GET_NETWORK_RESPONSE = requests.get(GET_NETWORK_URL, headers=HEADERS)
GET_NETWORK_JSON = GET_NETWORK_RESPONSE.json()

#pull back the status of all devices
GET_DEV_STS_URL = DASHBOARD + '/api/v0/organizations/%s/deviceStatuses' % ORGANIZATION
GET_DEV_STS_RSP = requests.get(GET_DEV_STS_URL, headers=HEADERS)
GET_DEV_STS_JSON = GET_DEV_STS_RSP.json()
#print(get_dev_sts_json)

for z in GET_DEV_STS_JSON:
    if z["status"] == "offline":
        down_id = z["networkId"]
        for i in GET_NETWORK_JSON:
            if down_id == i["id"] and REGEX.match(z["serial"]):
                print(i["name"] + ' ' + z["serial"])
            if down_id == i["id"] and REGEX1.match(z["serial"]):
                print(i["name"] + ' ' + z["serial"])
