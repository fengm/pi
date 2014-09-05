'''
File: auto_pilot.py
Author: Min Feng
Version: 0.1
Create: 2014-09-05 14:05:20
Description:
'''

import time
import threading
import logging

class auto_pilot (threading.Thread):
	def __init__(self, device='/dev/ttyACM0', baud=115200, delay=0.01):
		logging.info('init auto pilot module')
		threading.Thread.__init__(self)

		from pymavlink import mavutil
		self.mav = mavutil.mavlink_connection(device, baud=baud)

		logging.info('mav object type %s' % type(self.mav))
		logging.info('waiting for heart beat')
		self.mav.wait_heartbeat()

		self._loc = None
		self.running = False
		self.delay = 0.01

	def run(self):
		logging.info('start receiving')

		self.running = True
		while self.running:
			_loc = self.mav.location()

			_params = {'lon': _loc.lng, 'lat': _loc.lat, 'alt': _loc.alt, 'heading': _loc.heading}
			_params.update(self.mav.messages['VFR_HUD'].to_dict())

			self._loc = _params
			if self.delay > 0:
				time.sleep(self.delay)

	def stop(self):
		self.running = False

	@property
	def loc(self):
		return self._loc

def main():
	print 'init object'
	_obj = auto_pilot()
	print 'start receving'
	try:
		_obj.start()
		while True:
			if _obj.loc:
				for _k, _v in _obj.loc.items():
					print ' -', _k, _v
			time.sleep(0.5)
	except KeyboardInterrupt:
		print "User cancelled"
	except:
		import sys
		print "Unexpected error:", sys.exc_info()[0]
		raise
	finally:
		print "Stopping gps controller"
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
