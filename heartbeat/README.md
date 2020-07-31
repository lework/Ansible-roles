# Ansible Role: heartbeat

安装heartbeat，用于检查服务状态

## 介绍

Heartbeat是一个轻量级守护程序，您将其安装在远程服务器上以定期检查服务的状态并确定它们是否可用。与Metricbeat（仅告诉您服务器是关闭还是关闭）不同，Heartbeat会告诉您服务是否可以访问。

官方地址： https://www.elastic.co/products/beats/heartbeat
github: https://github.com/elastic/beats
官方文档地址：https://www.elastic.co/guide/en/beats/heartbeat/current/heartbeat-overview.html

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

heartbeat_version: "7.8.0"

heartbeat_service_status: started
heartbeat_service_enabled: yes

heartbeat_repo_install: true

heartbeat_conf_path: /etc/heartbeat/

heartbeat_conf:
  heartbeat.config.monitors:
    path: ${path.config}/monitors.d/*.yml
    reload.enabled: true
    reload.period: 10s
  setup.template.settings:
    index.number_of_shards: 0
    index.codec: best_compression
    _source.enabled: false
  output.elasticsearch:
    hosts: ["localhost:9200"]
  name: "{{ ansible_hostname | d(inventory_hostname)}}"
  logging.level: info
  http.enabled: false
  http.host: 0.0.0.0
  http.port: 5066
  
heartbeat_conf_file: ""

heartbeat_monitor_conf:
  - name: http
    conf:
      - type: http
        id: es-monitor
        name: "es Monitor"
        urls: ["http://localhost:9200"]
        schedule: '@every 10s'

heartbeat_setup: false
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/heartbeat

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - heartbeat
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`

```yaml
---

- hosts: node
  vars:
    - heartbeat_repo_install: false
    - __package_file: heartbeat-7.8.1-x86_64.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/beats/heartbeat/heartbeat-7.8.1-x86_64.rpm
  roles:
  - heartbeat
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - heartbeat_conf:
        heartbeat.config.monitors:
          path: ${path.config}/monitors.d/*.yml
          reload.enabled: true
          reload.period: 10s
        setup.template.settings:
          index.number_of_shards: 0
          index.codec: best_compression
          _source.enabled: false
        output.elasticsearch:
          hosts: ["localhost:9200"]
        name: "{{ ansible_hostname | d(inventory_hostname)}}"
        logging.level: info
        http.enabled: false
        http.host: 0.0.0.0
        http.port: 5066
    - heartbeat_monitor_conf:
        - name: http
          conf:
            - type: http
              id: es-monitor
              name: "es Monitor"
              urls: ["http://localhost:9200"]
              schedule: '@every 10s'
  roles:
  - heartbeat
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - heartbeat_conf_file: heartbeat-conf.yml
  roles:
  - heartbeat
```
