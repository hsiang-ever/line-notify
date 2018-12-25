#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from postLineNotify import postLineNotifiy

def getTaiwanOilPrice():
	url = 'https://gas.goodlife.tw/'
	r = requests.get(url)

	# r.encoding='utf-8'
	if r.status_code == requests.codes.ok:
		soup = BeautifulSoup(r.text, 'html.parser')

		gasolineInfo = {}
		# print(res.text)
		updatedTime = soup.find_all(string=re.compile('最後更新時間'))
		updatedTime = updatedTime[0].strip()[:-2]
		print(updatedTime)
		gasolineInfo['updatedTime'] = updatedTime

		# CPC_98,CPC_95,CPC_92,CPC_diesel,FPC_98,FPC_95,FPC_92,FPC_diesel
		idCpc = soup.find_all(id='cpc')
		cpc = []
		fpc = []
		for idCpcItem in idCpc:
			if idCpcItem.find_all("h2", string=re.compile("今日中油油價")):
				cpc = idCpcItem.find_all("h2", string=re.compile("今日中油油價"))
			elif idCpcItem.find_all("h2", string=re.compile("今日台塑油價")):
				fpc = idCpcItem.find_all("h2", string=re.compile("今日台塑油價"))
		# cpc = idCpc.find_all("h2", string=re.compile("今日中油油價"))
		cpcPriceul = cpc[0].find_next_sibling("ul")
		cpcGasType = cpcPriceul.find_all("h3")
		# for gasType in cpcGasType:
		# 	gasolineInfo['CPC' + (gasType.text.strip())[:-1]] = gasType.next_sibling.strip()
		gasolineInfo['CPC_92'] = cpcGasType[0].next_sibling.strip()
		gasolineInfo['CPC_95'] = cpcGasType[1].next_sibling.strip()
		gasolineInfo['CPC_98'] = cpcGasType[2].next_sibling.strip()
		gasolineInfo['CPC_diesel'] = cpcGasType[3].next_sibling.strip()
		fpcPriceul = fpc[0].find_next_sibling("ul")
		fpcGasType = fpcPriceul.find_all("h3")
		fpcGasPrice = fpcPriceul.find_all("li")
		# for gasType in fpcGasType:
		# 	gasolineInfo['FPC' + (gasType.text.strip())[:-1]] = gasType.next_sibling.strip()
		gasolineInfo['FPC_92'] = fpcGasType[0].next_sibling.strip()
		gasolineInfo['FPC_95'] = fpcGasType[1].next_sibling.strip()
		gasolineInfo['FPC_98'] = fpcGasType[2].next_sibling.strip()
		gasolineInfo['FPC_diesel'] = fpcGasType[3].next_sibling.strip()

		priceChange = soup.find_all(id='gas-price')[0]
		dieselText = priceChange.find_all("li", class_="alt")[0].find_all("h3")[0].text.strip()
		dieselPriceChange = priceChange.find_all("li", class_="alt")[0].find_all("h3")[0].next_sibling.strip().replace(" ", "")
		gasPriceChange = priceChange.find_all("li", class_="main")[0].find_all("h2")[0].text.strip()
		startedTime = priceChange.find_all("li", class_="main")[0].find_all("p")[0].text.strip()
		print(dieselText + ' ' + dieselPriceChange)
		# print(gasPriceChange)
		print(startedTime + ' ' + gasPriceChange)
		gasolineInfo['dieselPriceChangeNotify'] = dieselText + ' ' + dieselPriceChange
		gasolineInfo['gasPriceChangeNotify'] = startedTime + ' ' + gasPriceChange
		# print(gasolineInfo)
		return gasolineInfo
	else:
		print('notok')

def getFormattedGasolineMsg():
	gasolineInfo = getTaiwanOilPrice()
	message = '\n' + \
	gasolineInfo['updatedTime'] + '\n' + \
	gasolineInfo['gasPriceChangeNotify'] + '\n' + \
	gasolineInfo['dieselPriceChangeNotify'] + '\n' + \
	'中油油價:\n' + '92: ' + gasolineInfo['CPC_92'] + ', ' + \
	'95: ' + gasolineInfo['CPC_95'] + ', ' + \
	'98: ' + gasolineInfo['CPC_98'] + ', ' + \
	'柴油: ' + gasolineInfo['CPC_diesel'] + '\n' + \
	'台塑油價:\n' + '92: ' + gasolineInfo['FPC_92'] + ', ' + \
	'95: ' + gasolineInfo['FPC_95'] + ', ' + \
	'98: ' + gasolineInfo['FPC_98'] + ', ' + \
	'柴油: ' + gasolineInfo['FPC_diesel']
	return message

def sendGasolineMsgToLine():
	message = getFormattedGasolineMsg()
	payload={'message': message}
	postLineNotifiy(payload)