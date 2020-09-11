# Ansible Role: kapacitor

安装kapacitor

## 介绍
Kapacitor是InfluxData开源的数据处理引擎。它可以处理来自InfluxDB的流数据和批处理数据，并且用户可以用tickScript脚本来处理，监视和警报时序数据库中的时序数据。

官方地址：https://www.influxdata.com/time-series-platform/kapacitor/
github: https://github.com/influxdata/kapacitor
官方文档地址：https://docs.influxdata.com/kapacitor

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

kapacitor_version: "1.5.6"


# Service
kapacitor_service_status: started
kapacitor_service_enabled: yes

# Port
kapacitor_http_port: 9092

# Config
kapacitor_conf_path: /etc/kapacitor/
kapacitor_influxdb_url: ["http://localhost:8086"]

kapacitor_conf: |
  hostname = "{{ ansible_nodename |d ('localhost') }}"
  data_dir = "/var/lib/kapacitor"
  skip-config-overrides = false
  default-retention-policy = ""
  [http]
    bind-address = ":{{ kapacitor_http_port }}"
    log-enabled = true
    write-tracing = false
    pprof-enabled = false
    https-enabled = false
    https-certificate = "/etc/ssl/kapacitor.pem"
  [tls]
  [config-override]
    enabled = true
  [logging]
      file = "/var/log/kapacitor/kapacitor.log"
      level = "INFO"
  [load]
    enabled = true
    dir = "/etc/kapacitor/load"
  [replay]
    dir = "/var/lib/kapacitor/replay"
  [task]
    dir = "/var/lib/kapacitor/tasks"
    snapshot-interval = "60s"
  [storage]
    boltdb = "/var/lib/kapacitor/kapacitor.db"
  [[influxdb]]
    enabled = true
    default = true
    name = "default"
    urls = {{ kapacitor_influxdb_url | to_json }}
    username = ""
    password = ""
    timeout = 0
    insecure-skip-verify = false
    startup-timeout = "5m"
    disable-subscriptions = false
    subscription-mode = "cluster"
    subscription-protocol = "http"
    subscriptions-sync-interval = "1m0s"
    kapacitor-hostname = ""
    http-port = 0
    udp-bind = ""
    udp-buffer = 1000
    udp-read-buffer = 0
    [influxdb.subscriptions]
    [influxdb.excluded-subscriptions]
  [smtp]
    enabled = false
    host = "localhost"
    port = 25
    username = ""
    password = ""
    from = ""
    no-verify = false
    idle-timeout = "30s"
    global = false
    state-changes-only = false
  [stats]
    enabled = true
    stats-interval = "10s"
    database = "_kapacitor"
    retention-policy= "autogen"
  
kapacitor_conf_file: ""

```

发行版变量

```yaml

# Debian.yml
__package_file: kapacitor_{{ kapacitor_version }}-1_amd64.deb
__package_file_url: https://dl.influxdata.com/kapacitor/releases/{{ __package_file }}

# RedHat.yml
__package_file: kapacitor-{{ kapacitor_version }}-1.x86_64.rpm
__package_file_url: https://dl.influxdata.com/kapacitor/releases/{{ __package_file }}

```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/kapacitor

## Example Playbook

> 默认使用package包方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - kapacitor
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - kapacitor_conf: |
        hostname = "localhost"
        data_dir = "/var/lib/kapacitor"
        skip-config-overrides = false
        default-retention-policy = ""
        [http]
          bind-address = ":9092"
          log-enabled = true
          write-tracing = false
          pprof-enabled = false
          https-enabled = false
          https-certificate = "/etc/ssl/kapacitor.pem"
        [logging]
            file = "/var/log/kapacitor/kapacitor.log"
            level = "INFO"
        [load]
          enabled = true
          dir = "/etc/kapacitor/load"
        [replay]
          dir = "/var/lib/kapacitor/replay"
        [task]
          dir = "/var/lib/kapacitor/tasks"
          snapshot-interval = "60s"
        [storage]
          boltdb = "/var/lib/kapacitor/kapacitor.db"
        [[influxdb]]
          enabled = true
          default = true
          name = "default"
          urls = ["http://influxdb:8086"]
  roles:
  - kapacitor
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - kapacitor_conf_file: kapacitor-conf.conf
  roles:
  - kapacitor
```
