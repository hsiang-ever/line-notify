#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def sqlServerDbConnection():
	driver = config['SQL_SERVER_DB']['DRIVER']
	server_ip = config['SQL_SERVER_DB']['SERVER_IP']
	database = config['SQL_SERVER_DB']['DATABASE']
	username = config['SQL_SERVER_DB']['USERNAME']
	password = config['SQL_SERVER_DB']['PASSWORD']
	con = pyodbc.connect(driver=driver,server=server_ip,database=database,uid=username,pwd=password)
	return con
