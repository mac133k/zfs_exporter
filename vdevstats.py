import os
import re
from prometheus_client.core import GaugeMetricFamily

class VdevstatsCollector(object):
	def collect(self):
		# Load vdevcachestats from file
		vdevcachestats = {}
		vdevcachestats_f = '/proc/spl/kstat/zfs/vdev_cache_stats'
		lines = open(vdevcachestats_f, 'r').readlines() if os.path.isfile(vdevcachestats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			vdevcachestats[items[0]] = items[2]

		# Load vdevmirrorstats from file
		vdevmirrorstats = {}
		vdevmirrorstats_f = '/proc/spl/kstat/zfs/vdev_mirror_stats'
		lines = open(vdevmirrorstats_f, 'r').readlines() if os.path.isfile(vdevmirrorstats_f) else [0,0]
		for l in lines[2:]:
			items = re.split(r' +', l)
			vdevmirrorstats[items[0]] = items[2]

		# Metric declarations	
		CACHESTATS = GaugeMetricFamily('zfs_vdev_cache_stats', 'vdev cache statistics.', labels=['stat'])
		for label, value in vdevcachestats.items():
			CACHESTATS.add_metric([label], value)
		MIRRORSTATS = GaugeMetricFamily('zfs_vdev_mirror_stats', 'vdev mirror statistics.', labels=['stat'])
		for label, value in vdevmirrorstats.items():
			MIRRORSTATS.add_metric([label], value)

		yield CACHESTATS
		yield MIRRORSTATS
