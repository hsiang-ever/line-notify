#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import re

def getTaiwanOilPrice():
	url = 'http://www.taiwanoil.org/'
	res = requests.get(url)
	res.encoding='utf-8'

	soup = BeautifulSoup(res.text, 'html.parser')
	# print(res.text)
	updatedTime = soup.find_all(string=re.compile('更新時間'))
	updatedTime = updatedTime[0].strip()
	print(updatedTime)

	providedFerm = soup.find_all('td', style='text-align:right;')
	ferms = []
	for index in range(0, len(providedFerm), 5):
		ferms.append(providedFerm[index].text.strip())
	print(ferms)

	filteredPrices = []
	prices = soup.find_all('td', style='text-shadow:none;color:#0000ff;font-color:#0000ff;text-align:right;')
	for item in prices:
		filteredPrices.append(item.text.strip())
	print(filteredPrices)
	return (updatedTime, ferms, filteredPrices)

