from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class ArcstatsCollector(object):
	def collect(self):
		# Load arcstats from file
		arcstats = {}
		try:
			lines = open('/proc/spl/kstat/zfs/arcstats', 'r').readlines()
			for l in lines[2:]:
				items = re.split(r' +', l)
				arcstats[items[0]] = items[2]

		# Metric declarations	
		ARCSTATS = GaugeMetricFamily('zfs_arcstats', 'ARC statistics.', labels=arcstats.keys())
		for label, value in arcstats.iteritems():
			ARCSTATS.add_metric(label, value)

		yield ARCSTATS
