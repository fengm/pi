#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: get_ip_address.py
Author: Min Feng
Version: 0.1
Create: 2014-02-19 11:33:39
Description: Get and send out the ip address
'''

import logging

def get_ipv4_address():
	import subprocess

	_p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
	return _p.communicate()[0].strip()

def send_email(ip):
	import smtplib

	logging.info('sending email: %s' % ip)

	FROM = 'mfeng.geo@gmail.com'
	TO = ['min.fng@gmail.com']
	SUBJECT = "IP address"
	TEXT = ip

	_msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	_ser = smtplib.SMTP("smtp.gmail.com", 587)
	_ser.ehlo()
	_ser.starttls()

	import base64
	_b = base64.b64decode
	_ser.login(_b('bWZlbmcuZ2VvQGdtYWlsLmNvbQ=='), _b('eGlhb3lpbmc='))
	_ser.sendmail(FROM, TO, _msg)
	_ser.close()

	logging.info('email sent')

def main():
	_init_env()

	_ip = None

	import time
	while(True):
		try:
			_ip_v = get_ipv4_address()
			if not _ip_v:
				logging.warning('failed to get ip address')
				continue

			if _ip_v != _ip:
				_ip = _ip_v

				try:
					send_email(_ip)
				except KeyboardInterrupt, err:
					raise err
				except Exception, err:
					import traceback

					logging.error(traceback.format_exc())
					logging.error(str(err))
		finally:
			time.sleep(30)

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')

	return _p.parse_args()

def _init_env():
	import os, sys
	_d_in = os.path.join(sys.path[0], 'lib')
	if os.path.exists(_d_in):
		sys.path.append(_d_in)

	_opts = _usage()

	import logging_util
	logging_util.init(_opts.logging)

	import config
	config.load(_opts.config)

	return _opts

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print '\n\n* User stopped the program'
	except Exception, err:
		import traceback

		logging.error(traceback.format_exc())
		logging.error(str(err))

		print '\n\n* Error:', err

