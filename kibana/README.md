# Ansible Role: kibana

安装kibana

## 介绍
Kibana 是一个为 Logstash 和 ElasticSearch 提供的日志分析的 Web 接口。可使用它对日志进行高效的搜索、可视化、分析等各种操作。

官方地址： https://www.elastic.co/products/kibana
github: https://github.com/elastic/kibana
官方文档地址：https://www.elastic.co/guide/en/kibana/current/index.html

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

kibana_version: "7.8.1"

kibana_service_status: started
kibana_service_enabled: yes

kibana_repo_install: true

kibana_conf_path: /etc/kibana/

kibana_conf:
  server.port: 5601
  server.host: "0.0.0.0"
  elasticsearch.hosts: ["http://localhost:9200"]

kibana_conf_file: ""

kibana_plugin: []
kibana_plugin_file: []
```

## 依赖


## github地址
https://github.com/lework/Ansible-roles/tree/master/kibana

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - kibana
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`
```yaml
---

- hosts: node
  vars:
    - kibana_repo_install: false
    - __package_file: kibana-7.8.1.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/kibana/kibana-7.8.1.rpm
  roles:
  - kibana
```

### 指定配置

```yaml
---

- hosts: 192.168.77.160
  vars:
    - kibana_repo_install: false
    - kibana_conf:
        server.port: 5601
        server.host: "0.0.0.0"
        elasticsearch.hosts: ["http://localhost:9200"]
  roles:
  - kibana
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - kibana_conf_file: kibana.yml
  roles:
  - kibana
```

### 安装插件

```yaml
---

- hosts: node
  vars:
    - kibana_plugin:
      - https://github.com/sivasamyk/logtrail/releases/download/v0.1.31/logtrail-7.8.0-0.1.31.zip
    - kibana_plugin_file:
      - logtrail-7.8.0-0.1.31.zip
  roles:
  - kibana
```
