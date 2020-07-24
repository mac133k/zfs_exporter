import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class ZfetchstatsCollector(object):
	def collect(self):
		# Load zfetchstats from file
		zfetchstats = {}
		zfetchstats_f = '/proc/spl/kstat/zfs/zfetchstats'
		lines = open(zfetchstats_f, 'r').readlines() if os.path.isfile(zfetchstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			zfetchstats[items[0]] = items[2]

		print(zfetchstats)
		# Metric declarations	
		ZFETCHSTATS = GaugeMetricFamily('zfs_zfetchstats', 'ZFETCH statistics.', labels=['stat'])
		for label, value in zfetchstats.items():
			ZFETCHSTATS.add_metric([label], value)

		yield ZFETCHSTATS
