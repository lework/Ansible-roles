# Ansible Role: telegraf

安装telegraf，用于收集指标

## 介绍

Telegraf是一个插件驱动的服务器代理，用于从数据库，系统和IoT传感器收集和发送指标和事件。Telegraf使用Go编写的，并编译成一个单独的二进制文件，没有外部依赖关系，并且需要非常小的内存占用。

官方地址： https://www.influxdata.com/time-series-platform/telegraf/
github: https://github.com/influxdata/telegraf
官方文档地址：https://docs.influxdata.com/telegraf/

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

telegraf_version: "1.15.2"


# Service
telegraf_service_status: started
telegraf_service_enabled: yes

# Config
telegraf_conf_path: /etc/telegraf/
telegraf_influxdb_url: ["http://localhost:8086"] 

telegraf_conf: |
  [global_tags]
  
  [agent]
    interval = "10s"
    round_interval = true
    metric_batch_size = 1000
    metric_buffer_limit = 10000
    collection_jitter = "0s"
    flush_interval = "10s"
    flush_jitter = "0s"
    precision = ""
    hostname = ""
    omit_hostname = false
  
  [[inputs.cpu]]
    percpu = true
    totalcpu = true
    collect_cpu_time = false
    report_active = false
  [[inputs.disk]]
    ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
  [[inputs.diskio]]
  [[inputs.kernel]]
  [[inputs.mem]]
  [[inputs.processes]]
  [[inputs.swap]]
  [[inputs.system]]
  [[inputs.net]]
  [[inputs.netstat]]
  [[inputs.nstat]]
    proc_net_netstat = "/proc/net/netstat"
    proc_net_snmp = "/proc/net/snmp"
    proc_net_snmp6 = "/proc/net/snmp6"
    dump_zeros       = true
  [[inputs.conntrack]]
     files = ["ip_conntrack_count","ip_conntrack_max",
              "nf_conntrack_count","nf_conntrack_max"]
     dirs = ["/proc/sys/net/ipv4/netfilter","/proc/sys/net/netfilter"]
     
  [[outputs.influxdb]]
    urls = {{ telegraf_influxdb_url | to_json }}
    database = "telegraf"
    timeout = "5s"
  
telegraf_conf_file: ""

```

发行版变量

```yaml

# Debian.yml
__package_file: telegraf_{{ telegraf_version }}-1_amd64.deb
__package_file_url: https://dl.influxdata.com/telegraf/releases/{{ __package_file }}


# RedHat.yml
__package_file: telegraf-{{ telegraf_version }}-1.x86_64.rpm
__package_file_url: https://dl.influxdata.com/telegraf/releases/{{ __package_file }}
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/telegraf

## Example Playbook

> 默认使用package包方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - telegraf
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - telegraf_conf: |
        [global_tags]
        
        [agent]
          interval = "10s"
          round_interval = true
          metric_batch_size = 1000
          metric_buffer_limit = 10000
          collection_jitter = "0s"
          flush_interval = "10s"
          flush_jitter = "0s"
          precision = ""
          hostname = ""
          omit_hostname = false
        
        [[inputs.cpu]]
          percpu = true
          totalcpu = true
          collect_cpu_time = false
          report_active = false
        [[inputs.disk]]
          ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
        [[inputs.diskio]]
        [[inputs.kernel]]
        [[inputs.mem]]
        [[inputs.processes]]
        [[inputs.swap]]
        [[inputs.system]]
        [[inputs.net]]
        [[inputs.netstat]]
        [[inputs.nstat]]
          proc_net_netstat = "/proc/net/netstat"
          proc_net_snmp = "/proc/net/snmp"
          proc_net_snmp6 = "/proc/net/snmp6"
          dump_zeros       = true
        [[inputs.conntrack]]
           files = ["ip_conntrack_count","ip_conntrack_max",
                    "nf_conntrack_count","nf_conntrack_max"]
           dirs = ["/proc/sys/net/ipv4/netfilter","/proc/sys/net/netfilter"]
           
        [[outputs.influxdb]]
          urls = ["http://influxdb:9096"]
          database = "telegraf"
          timeout = "5s"
  roles:
  - telegraf
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - telegraf_conf_file: telegraf-conf.conf
  roles:
  - telegraf
```
