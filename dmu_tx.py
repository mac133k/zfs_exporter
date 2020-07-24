import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class DmutxCollector(object):
	def collect(self):
		# Load dmutxstats from file
		dmutxstats = {}
		dmutxstats_f = '/proc/spl/kstat/zfs/dmu_tx'
		lines = open(dmutxstats_f, 'r').readlines() if os.path.isfile(dmutxstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			dmutxstats[items[0]] = items[2]

		print(dmutxstats)
		# Metric declarations	
		DMUTXSTATS = GaugeMetricFamily('zfs_dmu_tx', 'DMU TX statistics.', labels=['stat'])
		for label, value in dmutxstats.items():
			DMUTXSTATS.add_metric([label], value)

		yield DMUTXSTATS
