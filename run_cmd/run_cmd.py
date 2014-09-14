
import logging

def run(cmd, retry, delay):
	cmd = cmd.strip()
	if not cmd:
		logging.warning('no cmd provided')
		return

	_vs = cmd.split(' ')

	import run_commands
	import os

	for i in xrange(retry):
		_f = os.path.abspath(_vs[0])

		if not os.path.exists(_f):
			import time
			time.sleep(delay)
			logging.info('waiting for %ss' % delay)
			continue

		_cmd = ' '.join(['python', '-u', _f] + list(_vs[1:]))
		logging.info('start cmd: %s' % _cmd)

		import sys
		_p = os.path.dirname(_f)

		_f_log = os.path.join(sys.path[0], 'log', 'cmd_std.log')
		with open(_f_log, 'w') as _f_opo:
			import config
			if config.cfg.getboolean('conf', 'background'):
				_out_log = _f_opo
				_err_log = _f_opo
			else:
				import sys
				_out_log = sys.stdout
				_err_log = sys.stderr

			run_commands.run(_cmd, True, cwd=_p, stdout=_out_log, stderr=_err_log)
		break

def main():
	_init_env()

	import config
	_cfg = config.cfg

	run(_cfg.get('cmd', 'cmd') if _cfg.has_option('cmd', 'cmd') else '', _cfg.getint('conf', 'retry'), _cfg.getfloat('conf', 'delay'))

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

