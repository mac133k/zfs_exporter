import os
import re
from prometheus_client.core import GaugeMetricFamily

class StatsCollector(object):
	"""
	Generic ZFS statistic collector.
	"""
	def __init__(self, path, m_pfx, m_desc):
		"""
		Initialized the collector object.
	
		Parameters
		----------
		path : str
			The full path to the metric file.
		m_pfx : str
			Prefix for the names of generated metrics.
		m_desc : str
			Metric description string that will be set for every metric from the file.
		"""
		self.path   = path
		self.m_pfx  = m_pfx
		self.m_desc = m_desc


	def collect(self):
		"""
		Collects metrics from the stats file. The expected syntax of the lines 
		with metric data has 3 columns, ie.:
	
		hits				4    168948958
		misses				4    4767869
		...
	
		Returns
		-------
		Yields metrics of the Gauge type.
		"""
		try:
			with open(self.path, 'r') as f:
				mline = re.compile('^[_a-z]+ +[0-9] +[0-9]+$')
				for l in f:
					if not mline.match(l):
						continue
					items = re.split(r' +', l)
					if len(items) != 3 and type(items[1]) == int:
						continue
					yield GaugeMetricFamily(self.m_pfx + items[0], self.m_desc, value=float(items[2]))
		except Exception as e:
			print('Error: {}'.format(str(e)))


class PoolstatsCollector(object):
	"""
	Per pool statistic collector.
	"""
	def __init__(self):
		self.states = { # valid pool states
				'ONLINE':	1.0,
				'DEGRADED':	0.2,
				'FAULTED':	0.1,
				'OFFLINE':	0.0,
				'UNAVAIL':	-1.0,
				'REMOVED':	-2.0
				}
			

	def get_state_num(self, state):
		"""
		Translates the state string into the corresponding float number
		or returns -3.0 if not found.
		"""
		return self.states[state] if state in self.states.keys() else -3.0 # UNKNOWN


	def collect(self):
		"""
		Discovers the pools by searching for folders in /proc/spl/kstat/zfs, 
		then extracts the state and IO stats from the files.

		Returns
		-------
		Yields metrics of the Gauge type.
		"""
		# Metric declarations	
		# Find the ZFS pools
		for pooldir in  [f.path for f in os.scandir('/proc/spl/kstat/zfs') if f.is_dir()]:
			poolname = pooldir.split('/')[-1]
			# Load state from file
			try:
				with open(pooldir + '/state', 'r') as f:
					for l in f:
						STATE = GaugeMetricFamily('zfs_pool_state', 'Pool state (ONLINE = 1, OFFLINE = 0)', labels=['pool'])
						STATE.add_metric([poolname], self.get_state_num(l.strip()))
						yield STATE
			except Exception as e:
				print('Error: {}'.format(str(e)))
			# Load IO stats from file
			iostats_p = pooldir + '/io'
			lines = open(iostats_p, 'r').readlines() if os.path.isfile(iostats_p) else []
			if len(lines) > 2:
				keys = re.split(r' +', lines[1].strip())
				vals = re.split(r' +', lines[2].strip())
				for (key, value) in zip(keys, vals):
					IOSTATS = GaugeMetricFamily('zfs_pool_io_' + key, 'Pool IO statistics', labels=['pool'])
					IOSTATS.add_metric([poolname], value)
					yield IOSTATS
