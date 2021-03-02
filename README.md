# zfs_exporter
ZFS metric exporter for Prometheus

## Note: Alternative available
ZFS metrics were added to [PCP v5.2.4](https://github.com/performancecopilot/pcp/tree/5.2.4) in Feb 2021. Metrics are collected via PMDA written in C by [@mac133k](https://github.com/mac133k) and include the same selection as this ZFS Exporter plus the new metrics introduced in OpenZFS v2. PCP suite supports OpenMetrics and provides Prometheus client, so I strongly recommend it to Linux users as it is a more robust solution, and provides a large number of monitoring tools and features. Switching from ZFS Exporter should be easy, because metric names follow the same convention.

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

# Running as a SystemD service
Having ZFS Exported set up as a SystemD unit makes it easy to make sure it starts automatically after system reboot. Assuming that it was installed in `/opt` one can create a service file in `/usr/lib/systemd/system/zfs-exporter.service` or some other path depending on the distro, ie.:
```
[Unit]
Description=ZFS metrics exporter for Prometheus

[Service]
Type=forking
ExecStart=/bin/bash /opt/zfs_exporter/start.sh
ExecStop=/bin/bash /opt/zfs_exporter/stop.sh
PIDFile=/opt/zfs_exporter/var/pid

[Install]
WantedBy=multi-user.target
```

Next run these few commands to complete the installation:
```
/opt/zfs_exporter/stop.sh # if needed
chmod 644 /usr/lib/systemd/system/zfs-exporter.service
systemctl daemon-reload
systemctl enable zfs-exporter
systemctl start zfs-exporter
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
Metrics are imported from the files in `/proc/spl/kstat/zfs/` and are generally named after the file they were extracted from with the `zfs_` prefix, ie. `zfs_arc_hits`, `zfs_arc_misses`, etc.
Additionally the per pool metrics `zfs_pool_state` and `zfs_pool_io_*` have additional label `pool` which holds the name of the corresponding pool. 

For the sake of simplicity each metric is of the gauge type with an unspecified unit, so it is up to the user to properly handle the semantics of interesing statistics where it comes to plotting them of graphs or referring to in alert rules etc.

# PromQL
Calculate the cache hit percentage:
```
100 * rate(zfs_arc_hits}[5m]) / (rate(zfs_arc_hits[5m]) + rate(zfs_arc_misses[5m]))
```
