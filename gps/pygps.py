
import time
import threading

class gps_mag(threading.Thread):

	def __init__(self):
		import gps

		threading.Thread.__init__(self)
		self.gpsd = gps.gps()
		# self.gpsd.stream(gps.WATCH_ENABLE |  gps.WATCH_NEWSTYLE)
		self.gpsd.stream(gps.WATCH_ENABLE)
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			self.gpsd.next()

	def stop(self):
		self.running = False

	@property
	def fix(self):
		return self.gpsd.fix

	@property
	def utc(self):
		return self.gpsd.utc

	@property
	def satellites(self):
		return self.gpsd.satellites

def main():
	gpsc = gps_mag()
	try:
		# start controller
		gpsc.start()
		while True:
			print "latitude ", gpsc.fix.latitude
			print "longitude ", gpsc.fix.longitude
			print "time utc ", gpsc.utc, " + ", gpsc.fix.time
			print "altitude (m)", gpsc.fix.altitude
			print "eps ", gpsc.fix.eps
			print "epx ", gpsc.fix.epx
			print "epv ", gpsc.fix.epv
			print "ept ", gpsc.gpsd.fix.ept
			print "speed (m/s) ", gpsc.fix.speed
			print "climb ", gpsc.fix.climb
			print "track ", gpsc.fix.track
			print "mode ", gpsc.fix.mode
			print "sats ", gpsc.satellites
			time.sleep(0.5)
	except KeyboardInterrupt:
		print "User cancelled"
	except:
		import sys
		print "Unexpected error:", sys.exc_info()[0]
		raise
	finally:
		print "Stopping gps controller"
		gpsc.stop()
		#wait for the tread to finish
		gpsc.join()

	print "Done"

def _init_env():
	import os, sys
	_d_in = os.path.join(sys.path[0], 'lib')
	if os.path.exists(_d_in):
		sys.path.append(_d_in)

if __name__ == '__main__':
	_init_env()
	main()

