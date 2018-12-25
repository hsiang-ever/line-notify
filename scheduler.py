#!/usr/bin/python
# -*- coding: UTF-8 -*-

import schedule
from GasolineWebsiteMsg import sendGasolineMsgToLine

schedule.every().sunday.at("12:30").do(sendGasolineMsgToLine)

print('Scheduler In!')
while True:
	schedule.run_pending()