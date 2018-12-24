#!/usr/bin/python
# -*- coding: UTF-8 -*-

import schedule
from postGoogleAppsScript import scheduleJob

schedule.every().sunday.at("6:00").do(scheduleJob)
print('Scheduler In!')
while True:
	schedule.run_pending()

