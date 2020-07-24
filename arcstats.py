import os
import re
from prometheus_client.core import GaugeMetricFamily

class ArcstatsCollector(object):
	def collect(self):
		# Load arcstats from file
		arcstats = {}
		arcstats_f = '/proc/spl/kstat/zfs/arcstats'
		lines = open(arcstats_f, 'r').readlines() if os.path.isfile(arcstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			arcstats[items[0]] = items[2]

		# Metric declarations	
		ARCSTATS = GaugeMetricFamily('zfs_arc_stats', 'ARC statistics.', labels=['stat'])
		for label, value in arcstats.items():
			ARCSTATS.add_metric([label], value)

		yield ARCSTATS
