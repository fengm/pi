'''
File: sensor_mag.py
Author: Min Feng
Version: 0.1
Create: 2014-09-05 16:35:21
Description:
'''

import logging

def generate_file_name(d):
	import os
	for i in xrange(100000):
		_f_out = os.path.join(d, 'file_%06d.csv' % i)
		if not os.path.exists(_f_out):
			return _f_out

def main():
	_init_env()

	import config, os, datetime

	print 'init modules'
	import optics
	_s_optic = optics.optics()

	import auto_pilot
	_s_autop = auto_pilot.auto_pilot()

	print 'testing signal'
	_s_optic.start()
	_s_autop.start()

	try:
		import time
		_pos = 0
		for i in xrange(config.cfg.getint('conf', 'max_try')):
			if None not in (_s_optic.values, _s_autop.loc):
				break

			_pos += 1
			print ' - tried #', _pos, _s_autop.loc == None, _s_optic.values == None
			logging.info(' - tried %s, %s, %s' % (_pos, _s_autop.loc == None, _s_optic.values == None))

			time.sleep(1)

		if None in (_s_optic.values, _s_autop.loc):
			raise Exception('failed to initialzied the modules')

		print 'start reading'

		_col = None
		_num = 0

		_delay = config.cfg.getfloat('conf', 'delay')

		_d_out = config.cfg.get('conf', 'output')
		os.path.exists(_d_out) or os.makedirs(_d_out)

		_f_out = generate_file_name(_d_out)
		with open(_f_out, 'w') as _fo:
			for i in xrange(config.cfg.getint('conf', 'max_num')):
				_val1 = _s_autop.loc
				_val2 = _s_optic.dicts

				_val = {'time': datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')}

				_val.update(_val1)
				_val.update(_val2)

				if _col == None:
					_col = ['time'] + sorted(_val1.keys()) + sorted(_val2.keys())
					_fo.write(','.join(_col))
					_fo.write('\n')

				_fo.write(','.join(map(str, [_val[_k] for _k in _col])))
				_fo.write('\n')
				_num += 1

				print '.',
				if _num % 10:
					import sys
					sys.stdout.flush()
					_fo.flush()

				time.sleep(_delay)

	except KeyboardInterrupt:
		print '\n\n* User stopped the program'

	except Exception, err:
		import traceback

		logging.error(traceback.format_exc())
		logging.error(str(err))

		print '\n\n* Error:', err
	finally:
		if _s_optic:
			_s_optic.stop()
		if _s_autop:
			_s_autop.stop()

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')
	_p.add_argument('--temp', dest='temp')

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

	import file_unzip as fz
	fz.clean(fz.default_dir(_opts.temp))

	return _opts

if __name__ == '__main__':
	main()

