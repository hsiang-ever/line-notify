#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import os
import time, datetime
from scrapGasoline import getTaiwanOilPrice

def callGoogleAppsScriptApi(api, payload):
	r = requests.post(api, data=payload)
	print(r.status_code, r.reason)
	print(r.text)

def scheduleJob():
	gasolineInfo = getTaiwanOilPrice()
	message = '\n' + gasolineInfo[0] + '\n'
	for index in range(len(gasolineInfo[1])):
		if index%4 == 0:
			message += '{0:7s} {1:>8s}\n'.format(gasolineInfo[1][index], (gasolineInfo[2][index]))
		else:
			message += '{0:7s} {1:>10s}\n'.format(gasolineInfo[1][index], (gasolineInfo[2][index]))
	print(message)
	payload={'msg': message}
	# google apps scritp can created in 'https://script.google.com/home'
	api = 'https://script.google.com/macros/s/AKfycbwlFb8Fg1_KMVIglQeQKpaXW7Gmv8wde1We3i075Ju81wqYTo8/exec'
	callGoogleAppsScriptApi(api, payload)

