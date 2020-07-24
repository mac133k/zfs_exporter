import os
import re
from prometheus_client.core import GaugeMetricFamily

class XuiostatsCollector(object):
	def collect(self):
		# Load xuiostats from file
		xuiostats = {}
		xuiostats_f = '/proc/spl/kstat/zfs/xuio_stats'
		lines = open(xuiostats_f, 'r').readlines() if os.path.isfile(xuiostats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			xuiostats[items[0]] = items[2]

		# Metric declarations	
		XUIOSTATS = GaugeMetricFamily('zfs_xuio_stats', 'XUIO statistics.', labels=['stat'])
		for label, value in xuiostats.items():
			XUIOSTATS.add_metric([label], value)

		yield XUIOSTATS
