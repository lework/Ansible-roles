# Ansible Role: metricbeat

安装metricbeat，用于收集服务指标

## 介绍

Metricbeat是一种轻量级的托运人，您可以将其安装在服务器上，以定期从操作系统和服务器上运行的服务收集指标。Metricbeat会收集它收集的度量标准和统计信息，并将其运送到您指定的输出，例如Elasticsearch或Logstash。

官方地址： https://www.elastic.co/products/beats/metricbeat
github: https://github.com/elastic/beats
官方文档地址：https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-overview.html

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

metricbeat_version: "7.8.0"

metricbeat_service_status: started
metricbeat_service_enabled: yes

metricbeat_repo_install: true

metricbeat_conf_path: /etc/metricbeat/

metricbeat_conf:
  metricbeat.config.modules:
    path: ${path.config}/modules.d/*.yml
    reload.enabled: false
  setup.template.settings:
    index.number_of_shards: 0
    index.codec: best_compression
  fields:
    env: staging
  output.elasticsearch:
    hosts:  ["localhost:9200"]
  http.enabled: false
  http.host: 0.0.0.0
  http.port: 5066
  
metricbeat_conf_file: ""

metricbeat_module_conf:
  - name: elasticsearch
    conf:
      - module: elasticsearch
        metricsets:
          - node
          - node_stats
        period: 10s
        hosts: ["http://localhost:9200"]

metricbeat_setup: false
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/metricbeat

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - metricbeat
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`

```yaml
---

- hosts: node
  vars:
    - metricbeat_repo_install: false
    - __package_file: metricbeat-7.8.1-x86_64.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.8.1-x86_64.rpm
  roles:
  - metricbeat
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - metricbeat_conf:
        metricbeat.config.modules:
          path: ${path.config}/modules.d/*.yml
          reload.enabled: false
        setup.template.settings:
          index.number_of_shards: 0
          index.codec: best_compression
        fields:
          env: staging
        setup.dashboards.enabled: true
        output.elasticsearch:
          hosts:  ["localhost:9200"]
        http.enabled: false
        http.host: 0.0.0.0
        http.port: 5066
    - metricbeat_module_conf:
        - name: elasticsearch
          conf:
            - module: elasticsearch
              metricsets:
                - node
                - node_stats
              period: 10s
              hosts: ["http://localhost:9200"]
  roles:
  - metricbeat
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - metricbeat_conf_file: metricbeat-conf.yml
  roles:
  - metricbeat
```
