# Ansible Role: influxdb

安装influxdb，

## 介绍
nfluxDB是一个开源时间序列平台。 这包括用于存储和查询数据，在后台处理数据以实现ETL或监视和警报目的的API，用户仪表板以及可视化和探索数据的API等。

官方地址：https://www.influxdata.com/products/influxdb-overview/
github:  https://github.com/influxdata/influxdb
官方文档地址：https://docs.influxdata.com/influxdb/

## 要求

此角色仅在RHEL或Debian及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量
```yaml
software_files_path: "/opt/software"
software_install_path: "/usr/local"

influxdb_version: "1.8.2"


# Service
influxdb_service_status: started
influxdb_service_enabled: yes

# Port
influxdb_http_port: 8086
influxdb_rpc_port: 8088
influxdb_udp_port: 8089

# Config
influxdb_conf_path: /etc/influxdb/

influxdb_conf: |
  reporting-disabled = false
  bind-address = ":{{ influxdb_rpc_port }}"
  [meta]
    dir = "/var/lib/influxdb/meta"
    retention-autocreate = true
    logging-enabled = true
  [data]
    dir = "/var/lib/influxdb/data"
    wal-dir = "/var/lib/influxdb/wal"
    query-log-enabled = true
    cache-max-memory-size = "1g"
    cache-snapshot-memory-size = "25m"
    cache-snapshot-write-cold-duration = "10m"
    compact-full-write-cold-duration = "4h"
    max-series-per-database = 1000000
    max-values-per-tag = 100000
    series-id-set-cache-size = 100
  [coordinator]
    write-timeout = "10s"
    max-concurrent-queries = 0
    query-timeout = "0s"
    log-queries-after = "10s"
    max-select-point = 0
    max-select-series = 0
    max-select-buckets = 0
  [retention]
    enabled = true
    check-interval = "30m"
  [shard-precreation]
    enabled = true
    check-interval = "10m"
    advance-period = "30m"
  [monitor]
    store-enabled = true
    store-database = "_internal"
    store-interval = "10s"
  [http]
    enabled = true
    flux-enabled = true
    flux-log-enabled = true
    bind-address = ":{{ influxdb_http_port }}"
    auth-enabled = false
    realm = "InfluxDB"
    log-enabled = true
    write-tracing = true
    pprof-enabled = true
    https-enabled = false
    https-certificate = "/etc/ssl/influxdb.pem"
    https-private-key = ""
    max-row-limit = 0
    max-connection-limit = 0
    bind-socket = "/var/run/influxdb.sock"
  [logging]
    format = "auto"
    level = "info"
    suppress-logo = false
  [subscriber]
    enabled = true
    http-timeout = "30s"
    insecure-skip-verify = false
    ca-certs = ""
    write-concurrency = 40
    write-buffer-size = 1000
  [[graphite]]
  [[collectd]]
  [[opentsdb]]
  [[udp]]
    enabled = true
    bind-address = ":{{ influxdb_udp_port }}"
    database = "udp"
    retention-policy = ""
    precision = ""
    batch-size = 5000
    batch-pending = 10
    batch-timeout = "1s"
    read-buffer = 0
  [continuous_queries]
    enabled = true
    log-enabled = true
    run-interval = "1s"
  [tls]
  
influxdb_conf_file: ""

```

发行版变量

```yaml

# Debian.yml
__package_file: influxdb_{{ influxdb_version }}_amd64.deb
__package_file_url: https://dl.influxdata.com/influxdb/releases/{{ __package_file }}


# RedHat.yml
__package_file: influxdb-{{ influxdb_version }}.x86_64.rpm
__package_file_url: https://dl.influxdata.com/influxdb/releases/{{ __package_file }}
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/influxdb

## Example Playbook

> 默认使用package包方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - influxdb
```


### 指定配置

```yaml
---

- hosts: node
  vars:
    - influxdb_conf: |
        reporting-disabled = false
        bind-address = ":{{ influxdb_rpc_port }}"
        [meta]
          dir = "/var/lib/influxdb/meta"
          retention-autocreate = true
          logging-enabled = true
        [data]
          dir = "/var/lib/influxdb/data"
          wal-dir = "/var/lib/influxdb/wal"
          query-log-enabled = true
          cache-max-memory-size = "1g"
          cache-snapshot-memory-size = "25m"
          cache-snapshot-write-cold-duration = "10m"
          compact-full-write-cold-duration = "4h"
          max-series-per-database = 1000000
          max-values-per-tag = 100000
          series-id-set-cache-size = 100
        [http]
          enabled = true
          flux-enabled = true
          flux-log-enabled = true
          bind-address = ":8086"
  roles:
  - influxdb
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - influxdb_conf_file: influxdb-conf.conf
  roles:
  - influxdb
```
