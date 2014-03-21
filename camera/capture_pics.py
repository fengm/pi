#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File: capture_pics.py
Author: Min Feng
Version: 0.1
Create: 2014-03-21 16:54:41
Description: capture photos on Raspberry PI
'''

import logging

def retrieve_gps():
	pass

def test1():
	print 'eeeee'

def check_output(d_out):
	import os

	_num = 0
	for _root, _dirs, _files in os.walk(d_out):
		for _file in _files:
			if _file.endswith('.jpg'):
				_num += 1

	logging.info('found %s pictures' % _num)
	return _num

def capture_pic(f_ot):
	import config
	_cfg = config.cfg

	_cmd = _cfg.get('conf', 'cmd') % (f_ot, )
	logging.info('cmd: %s' % _cmd)

	import run_commands
	return run_commands.run(_cmd)[0]

def delay_time(t_s, delay):
	import time

	_t = time.time()
	while _t - t_s < delay:
		time.sleep(0.1)
		_t = time.time()

	return _t

def main():
	_opts = _init_env()
	del _opts

	import config
	_cfg = config.cfg

	_max_file = _cfg.getint('conf', 'max_files')
	_time_delay = _cfg.getfloat('conf', 'time_delay')
	_d_out = _cfg.get('conf', 'output_dir')

	import time
	import os

	if os.path.exists(_d_out):
		if _cfg.getboolean('conf', 'clean_output'):
			print 'cleaning output'

			import shutil
			shutil.rmtree(_d_out)

	os.path.exists(_d_out) or os.makedirs(_d_out)

	_t_p = time.time()

	while(True):

		_num = check_output(_d_out)
		if _num > _max_file:
			print 'reach maximum files'
			break

		print ' +', _num, time.ctime(_t_p)
		if capture_pic(os.path.join(_d_out, 'image_%06d.jpg' % _num)) != 0:
			print 'error running raspistill'
			break

		_t_p = delay_time(_t_p, _time_delay)

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
	main()
