import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class ZilstatsCollector(object):
	def collect(self):
		# Load zilstats from file
		zilstats = {}
		zilstats_f = '/proc/spl/kstat/zfs/zil'
		lines = open(zilstats_f, 'r').readlines() if os.path.isfile(zilstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			zilstats[items[0][4:]] = items[2] # skip the 'zil_' prefix in labels

		print(zilstats)
		# Metric declarations	
		ZILSTATS = GaugeMetricFamily('zfs_zilstats', 'ZIL statistics.', labels=['stat'])
		for label, value in zilstats.items():
			ZILSTATS.add_metric([label], value)

		yield ZILSTATS
