'''
File: optics.py
Author: Min Feng
Version: 0.1
Create: 2014-09-05 16:14:44
Description:
'''

import time
import threading
import logging

class optics(threading.Thread):
	def __init__(self, integ=100, delay=0.01):
		import hs_sensor

		logging.info('init optics module')
		threading.Thread.__init__(self)

		self.bands = hs_sensor.init(integ)

		self.values = None
		self.dicts = None
		self.running = False

		self.delay = delay

	def run(self):
		import hs_sensor

		logging.info('start receiving')

		_vals = hs_sensor.farray(self.bands)
		_wavs = hs_sensor.farray(self.bands)

		self.running = True
		while self.running:
			hs_sensor.read(self.bands, _vals, _wavs)

			self.valus = _vals
			self.waves = _wavs

			self.values = [(_wavs[_b], _vals[_b]) for _b in xrange(self.bands)]

			_ds = {}
			for i in xrange(self.bands):
				_ds['w%04d' % i] = self.values[i][0]
				_ds['v%04d' % i] = self.values[i][1]

			self.dicts = _ds

			if self.delay > 0:
				time.sleep(self.delay)

	def stop(self):
		self.running = False

		import hs_sensor
		hs_sensor.close()

def main():
	print 'init object'
	_obj = optics()
	print 'start receving'
	try:
		_obj.start()
		while True:
			if _obj.values == None:
				continue

			for _v in _obj.values:
				print ' -', _v[0], _v[1]

			time.sleep(2)

	except KeyboardInterrupt:
		print "User cancelled"
	except:
		import sys
		print "Unexpected error:", sys.exc_info()[0]
		raise
	finally:
		print "Stopping controller"
		_obj.stop()
		#wait for the tread to finish
		# _obj.join()

	print "Done"

def _init_env():
	import os, sys
	_d_in = os.path.join(sys.path[0], 'lib')
	if os.path.exists(_d_in):
		sys.path.append(_d_in)

if __name__ == '__main__':
	_init_env()
	main()
