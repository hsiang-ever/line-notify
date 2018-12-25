#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from scrapGasoline import getTaiwanOilPrice
from postLineNotify import postLineNotifiy
from dbConnection import sqlServerDbConnection
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def getAdjustPriceInfo(gasolineInfo):
	lastWeekNo = ((int)(datetime.datetime.now().strftime("%U"))) -1
	db_con = sqlServerDbConnection()
	db_cur = db_con.cursor()
	db_cur.execute("SELECT TOP(1) * FROM dbo." + config['SQL_SERVER_DB']['TABLE'] + " WHERE week_no = ? ORDER BY sno DESC", lastWeekNo)
	row = db_cur.fetchone()
	adjustPriceInfo = []
	adjustPriceInfo.append((float)(gasolineInfo[2][1]) - row.CPC_98)
	adjustPriceInfo.append((float)(gasolineInfo[2][2]) - row.CPC_95)
	adjustPriceInfo.append((float)(gasolineInfo[2][3]) - row.CPC_92)
	adjustPriceInfo.append((float)(gasolineInfo[2][4]) - row.CPC_diesel)
	adjustPriceInfo.append((float)(gasolineInfo[2][5]) - row.FPC_98)
	adjustPriceInfo.append((float)(gasolineInfo[2][6]) - row.FPC_95)
	adjustPriceInfo.append((float)(gasolineInfo[2][7]) - row.FPC_92)
	adjustPriceInfo.append((float)(gasolineInfo[2][8]) - row.FPC_diesel)
	return adjustPriceInfo

def sendFormattedMsgToLine(gasolineInfo, adjustPriceInfo):
	message = '\n' + gasolineInfo[0] + '\n'
	for index in range(len(gasolineInfo[1])):
		if index%4 == 0:
			if index == 0:
				message += '{0:5s} {1:>7s} {2:>7s}\n'.format(gasolineInfo[1][index], (gasolineInfo[2][index]), '調整')
			else:
				message += '{0:5s} {1:>8s} {2:+12.2f}\n'.format(gasolineInfo[1][index], (gasolineInfo[2][index]), adjustPriceInfo[index-1])
		else:
			message += '{0:5s} {1:>11s} {2:+11.2f}\n'.format(gasolineInfo[1][index], (gasolineInfo[2][index]), adjustPriceInfo[index-1])
	print(message)
	payload={'message': message}
	postLineNotifiy(payload)

def saveGasolineInfoIntoDb(gasolineInfo):
	week = (str)(datetime.date.today().weekday())
	print(week)
	def weekdayText(x):
	    return {
	        '0': 'Monday',
	        '1': 'Tuesday',
	        '2': 'Wednesday',
	        '3': 'Thursday',
	        '4': 'Friday',
	        '5': 'Saturday',
	        '6': 'Sunday',
	    }.get(x, 'unknown')

	weekday = weekdayText(week)

	db_con = sqlServerDbConnection()
	db_cur = db_con.cursor()
	db_cmd = "INSERT INTO dbo." + config['SQL_SERVER_DB']['TABLE'] + "(day, week_no, created_time,CPC_98,CPC_95,CPC_92,CPC_diesel,FPC_98,FPC_95,FPC_92,FPC_diesel) values (?,?,?,?,?,?,?,?,?,?,?)"
	db_cur.execute(db_cmd, weekday, (int)(datetime.datetime.now().strftime("%U")), datetime.datetime.now(), gasolineInfo[2][1], gasolineInfo[2][2], gasolineInfo[2][3], gasolineInfo[2][4], gasolineInfo[2][5], gasolineInfo[2][6], gasolineInfo[2][7], gasolineInfo[2][8])
	db_con.commit()

def sendAndSaveGasolineMsg():
	gasolineInfo = getTaiwanOilPrice()
	adjustPriceInfo = getAdjustPriceInfo(gasolineInfo)
	sendFormattedMsgToLine(gasolineInfo, adjustPriceInfo)
	saveGasolineInfoIntoDb(gasolineInfo)