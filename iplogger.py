#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from ipify import get_ip
from ipify.exceptions import IpifyException
import logging

logging.basicConfig(level=logging.INFO,
	format='%(asctime)s %(message)s',
	datefmt='[%m/%d/%Y %H:%M:%S]',
	filename='iplog.log',
	filemode='a+')

try:
	ip = get_ip()
except IpifyException:
	logging.error('Unable to retrieve IP from ipify services.')
except Exception as e:
	logging.error('An unknown error occurred while trying to retrieve the IP.')
	logging.error(str(e))

iplist = [re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b$',line) 
			for line in open('iplog.log')]
iplist = [x for x in iplist if x != []]

try:
	if iplist[-1] != ip:
		logging.info('New IP is %s' % ip)
except IndexError:
	logging.info('Start IP is %s' % ip)
