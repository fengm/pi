
def output(d_ot, nu, rs, vs):
    import datetime, os

    _d = datetime.datetime.now()
    _f = os.path.join(d_ot, _d.strftime('%Y%m%d_%H%M%S_%f.csv'))

    _l = ['pixel,ref,val']
    for i in xrange(nu):
        _l.append('%4d,%5.2f,%1.2f' % (i+1, rs[i], vs[i]))

    with open(_f, 'w') as _fo:
        _fo.write('\n'.join(_l))

def main():
	_opts = _init_env()

	import hs_sensor, os

	_d_ot = _opts.output
	os.path.exists(_d_ot) or os.makedirs(_d_ot)

	hs_sensor.s_init()
	_vs = hs_sensor.farray(3000)
	_rs = hs_sensor.farray(3000)

	import time
	for _t in xrange(100):
		_ts = time.time()
		_nu = hs_sensor.s_read(_vs, _rs)
		output(_d_ot, _nu, _rs, _vs)

		_td = (time.time() - _ts)
		if _td < 0.1:
			time.sleep(0.1 - _td)

		print '>', _t, _td

	hs_sensor.s_close()

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')
	_p.add_argument('--temp', dest='temp')

	_p.add_argument('-o', '--output', dest='output', required=True)

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

