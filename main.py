import os
from flask import Flask, Response
from prometheus_client import multiprocess, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

app = Flask('zfs_exporter')

import arcstats

REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.register(arcstats.ArcstatsCollector())

@app.route('/')
def status():
	return Response('PID: {}\n'.format(os.getpid()))


@app.route('/metrics')
def metrics():
	multiprocess.MultiProcessCollector(REGISTRY)
	return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)
