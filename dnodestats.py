import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class DnodestatsCollector(object):
	def collect(self):
		# Load dnodestats from file
		dnodestats = {}
		dnodestats_f = '/proc/spl/kstat/zfs/dnodestats'
		lines = open(dnodestats_f, 'r').readlines() if os.path.isfile(dnodestats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			dnodestats[items[0]] = items[2]

		# Metric declarations	
		DNODESTATS = GaugeMetricFamily('zfs_dnode_stats', 'DNODE statistics.', labels=['stat'])
		for label, value in dnodestats.items():
			DNODESTATS.add_metric([label], value)

		yield DNODESTATS
