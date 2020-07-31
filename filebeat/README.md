# Ansible Role: filebeat

安装filebeat，用于收集日志

## 介绍
filebeat最初是基于logstash-forwarder源码的日志数据shipper。Filebeat安装在服务器上作为代理来监视日志目录或特定的日志文件，可以将日志转发到Logstash进行解析，也可以直接发送到Elasticsearch进行索引。

官方地址： https://www.elastic.co/products/beats/filebeat
github: https://github.com/elastic/beats
官方文档地址：https://www.elastic.co/guide/en/beats/filebeat/current/index.html

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

filebeat_version: "7.8.0"

filebeat_service_status: started
filebeat_service_enabled: yes

filebeat_repo_install: true

filebeat_conf_path: /etc/filebeat/

filebeat_conf:
  filebeat.config.modules:
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
  
filebeat_conf_file: ""

filebeat_module_conf:
  - name: system
    conf:
      - module: system
        syslog:
          enabled: true
        auth:
          enabled: true

filebeat_setup: false
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/filebeat

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - filebeat
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`

```yaml
---

- hosts: node
  vars:
    - filebeat_repo_install: false
    - __package_file: filebeat-7.8.0-x86_64.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.8.0-x86_64.rpm
  roles:
  - filebeat
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - filebeat_conf:
        filebeat.config.modules:
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
    - filebeat_module_conf:
      - name: system
        conf:
          - module: system
            syslog:
              enabled: true
            auth:
              enabled: true
  roles:
  - filebeat
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - filebeat_conf_file: filebeat-conf.yml
  roles:
  - filebeat
```
