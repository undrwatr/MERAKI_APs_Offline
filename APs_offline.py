#!/usr/bin/env python3


#Program to audit the store network and look for APs that are offline

#imports
import re
import requests

#Import the CRED module from a separate directory ****Only Usable when I run this script locally
import cred

#This pulls the information based on s/ns that start with these.
regex = re.compile('Q2PD')
regex1 = re.compile('Q2HD')

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key
hub = cred.hub

#Main URL for the Meraki Platform
dashboard = "https://dashboard.meraki.com"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#Pull back all of the network IDs:
get_network_url = dashboard + '/api/v0/organizations/%s/networks' % organization
get_network_response = requests.get(get_network_url, headers=headers)
get_network_json = get_network_response.json()

#pull back the status of all devices
get_dev_sts_url = dashboard + '/api/v0/organizations/%s/deviceStatuses' % organization
get_dev_sts_rsp = requests.get(get_dev_sts_url, headers=headers)
get_dev_sts_json = get_dev_sts_rsp.json()
#print(get_dev_sts_json)

for z in get_dev_sts_json:
    if z["status"] == "offline":
        down_id = z["networkId"]
        for i in get_network_json:
            if down_id == i["id"] and regex.match(z["serial"]):
                print(i["name"] + ' ' + z["serial"])
            if down_id == i["id"] and regex1.match(z["serial"]):
                print(i["name"] + ' ' + z["serial"])
