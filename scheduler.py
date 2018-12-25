#!/usr/bin/python
# -*- coding: UTF-8 -*-

import schedule
from sendAndSaveGasolineMsg import sendAndSaveGasolineMsg

schedule.every().sunday.at("12:00").do(sendAndSaveGasolineMsg)

print('Scheduler In!')
while True:
	schedule.run_pending()