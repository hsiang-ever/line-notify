#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def postLineNotifiy(payload):
	r = requests.post(config['LINE_NOTIFY_API']['API'], data=payload, headers={"Authorization": "Bearer " + config['LINE_PERSONAL_TOKEN']['FAMILY']})
	# r = requests.post(config['LINE_NOTIFY_API']['API'], data=payload, headers={"Authorization": "Bearer " + config['LINE_PERSONAL_TOKEN']['SELF']})
	print("Response payload: " + r.text)
	if r.status_code == 200:
		jsonRes = json.loads(r.text)
		print(jsonRes)
	else:
		print(r.reason)

