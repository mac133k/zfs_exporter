import os
import re
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class DbufstatsCollector(object):
	def collect(self):
		# Load dbufstats from file
		dbufstats = {}
		dbufstats_f = '/proc/spl/kstat/zfs/dbufstats'
		lines = open(dbufstats_f, 'r').readlines() if os.path.isfile(dbufstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			dbufstats[items[0]] = items[2]

		print(dbufstats)
		# Metric declarations	
		DBUFSTATS = GaugeMetricFamily('zfs_dbufstats', 'DBUF statistics.', labels=['stat'])
		for label, value in dbufstats.items():
			DBUFSTATS.add_metric([label], value)

		yield DBUFSTATS
