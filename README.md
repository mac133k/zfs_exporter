# zfs_exporter
ZFS metric exporter for Prometheus

# Overview
Small app that uses Python Prometheus Client to serve ZSF metrics to Prometheus or other compatible metric collector. It is designed to run on Linux servers and it takes all metrics from /proc.

# Installation
To install ZFS Exporter follow these steps:

```
pip3 install prometheus_client gunicorn flask
git clone https://github.com/mac133k/zfs_exporter.git
cd zfs_exporter
cp conf/env.sh.template conf/env.sh
```
 
# Starting and stopping
Use the scripts provided:
```
./start.sh
```
```
./stop.sh
```

# Testing
Check the URL to make sure the app is running:
```
curl localhost:20080/metrics
```
The pid file is the local `var` folder, the logs in `var/log/messages.log`.

# Prometheus configuration
Add the scrape job to your Prometheus config file:
```
- job_name: zsfstats
  honor_timestamps: true
  scrape_interval: 1m
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  static_configs:
  - targets: [...]
```

# Metrics
Metrics are imported from the files in `/proc/spl/kstat/zfs/` and are generally named after the file they were extracted from with the `zfs_` prefix. The names of individual items from each stat file appear as 'stat' label values, ie.:
```
zfs_arc_stats{stat='hits'}
```
Additionally the per pool metrics `zfs_pool_state` and `zfs_pool_io` have additional label `pool` which holds the name of the corresponding pool. 

For the sake of simplicity each metric is of the gauge type with an unspecified unit, so it is up to the user to properly handle the semantics of interesing statistics where it comes to plotting them of graphs or referring to in alert rules etc.

# PromQL
Due to the fact that the metrics are identified by the value of the `stat` label it is sometimes necessary to add the `ignoring(stat)` operator, ie. when calculating the cache hit percentage:
```
100 * rate(zfs_arc_stats{stat='hits'}[5m]) / ignoring(stat) (rate(zfs_arc_stats{stat='hits'}[5m]) + ignoring(stat) rate(zfs_arc_stats{stat='misses'}[5m]))
```

