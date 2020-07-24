import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class AbdstatsCollector(object):
	def collect(self):
		# Load abdstats from file
		abdstats = {}
		abdstats_f = '/proc/spl/kstat/zfs/abdstats'
		lines = open(abdstats_f, 'r').readlines() if os.path.isfile(abdstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			abdstats[items[0]] = items[2]

		# Metric declarations	
		ABDSTATS = GaugeMetricFamily('zfs_abdstats', 'ABD statistics.', labels=['stat'])
		for label, value in abdstats.items():
			ABDSTATS.add_metric([label], value)

		yield ABDSTATS
