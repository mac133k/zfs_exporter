import os
from flask import Flask, Response
from prometheus_client import multiprocess, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

app = Flask('zfs_exporter')

from zfx_collectors import StatsCollector, PoolstatsCollector

REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/arcstats',		'zfs_arc_',		'ARC statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/abdstats',		'zfs_abd_',		'ABD statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/dbufstats',		'zfs_dbuf_',		'DBUF statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/dnodestats',		'zfs_',			'DNode statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/dmu_tx',  		'zfs_',			'DMU TX statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/vdev_cache_stats',	'zfs_vdev_cache_',	'VDev cache statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/vdev_mirror_stats',	'zfs_vdev_mirror_',	'VDev mirror statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/xuio_stats',		'zfs_xuio_',		'XUIO statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/zfetchstats',		'zfs_zfetch_',		'ZFetch statistics'))
REGISTRY.register(StatsCollector('/proc/spl/kstat/zfs/zil',			'zfs_',		     	'ZIL statistics'))
REGISTRY.register(PoolstatsCollector())


@app.route('/')
def status():
	return Response('ZFS Exporter is running (PID: {})\n'.format(os.getpid()))


@app.route('/metrics')
def metrics():
	multiprocess.MultiProcessCollector(REGISTRY)
	return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)
