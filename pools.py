import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class PoolstatsCollector(object):
	def collect(self):
		# Metric declarations	
		STATE = GaugeMetricFamily('zfs_pool_state', 'Pool state (1 = ONLINE)', labels=['pool'])
		IOSTATS = GaugeMetricFamily('zfs_pool_io', 'Pool IO statistics.', labels=['pool', 'stat'])
		# Find the ZFS pools
		for pooldir in  [f.path for f in os.scandir('/proc/spl/kstat/zfs') if f.is_dir()]:
			poolname = pooldir.split('/')[-1]
			# Load state from file
			state_f = pooldir + '/state'
			lines = open(state_f, 'r').readlines() if os.path.isfile(state_f) else []
			if len(lines):
				STATE.add_metric([poolname], 1 if lines[0].strip() == 'ONLINE' else 0)
			# Load IO stats from file
			iostats_f = pooldir + '/io'
			lines = open(iostats_f, 'r').readlines() if os.path.isfile(iostats_f) else []
			if len(lines) > 2:
				keys = re.split(r' +', lines[1].strip())
				vals = re.split(r' +', lines[2].strip())
				for (key, value) in zip(keys, vals):
					IOSTATS.add_metric([poolname, key], value)
		yield STATE
		yield IOSTATS
