# Ansible Role: elasticsearch

安装elasticsearch

## 介绍

ElasticSearch是一个基于Lucene的搜索服务器。它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是当前流行的企业级搜索引擎。设计用于云计算中，能够达到实时搜索，稳定，可靠，快速，安装使用方便。

官方地址： https://www.elastic.co/products/elasticsearch
github: https://github.com/elastic/elasticsearch
官方文档地址：https://www.elastic.co/guide/en/elasticsearch/current/index.html

## 要求

此角色仅在RHEL或Debian及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量
```yaml
---
# author: lework

software_files_path: "/opt/software"
software_install_path: "/usr/local"

elasticsearch_version: "7.8.1"

elasticsearch_service_status: started
elasticsearch_service_enabled: yes

elasticsearch_repo_install: true


elasticsearch_data_paths:
  - "/var/lib/elasticsearch"
elasticsearch_log_path: "/var/log/elasticsearch"
elasticsearch_heap_dump_path: "/var/lib/elasticsearch"
elasticsearch_conf_path: "/etc/elasticsearch"
elasticsearch_systemd_config_file: "/etc/systemd/system/elasticsearch.service.d/override.conf"


elasticsearch_conf: []
elasticsearch_conf_file: ""
elasticsearch_log4j2_file: ""

elasticsearch_plugin: []
elasticsearch_plugin_file: []

elasticsearch_user: elasticsearch
elasticsearch_group: elasticsearch

elasticsearch_http_host: "0.0.0.0"
elasticsearch_http_port: 9200

elasticsearch_max_open_files: 655350
elasticsearch_max_map_count: 262144

elasticsearch_cluster_name: ""
elasticsearch_node_name: ""

elasticsearch_scripts_fileglob: ""
elasticsearch_install_plugins: []

elasticsearch_heap_size: "1g"
elasticsearch_java_home: ""

# xpack
elasticsearch_xpack_enable: false
elasticsearch_ssl_cert_generate: false
elasticsearch_enable_http_ssl: false
elasticsearch_enable_transport_ssl: false
elasticsearch_ssl_certificate_path: "{{ elasticsearch_conf_path }}/certs"
elasticsearch_ssl_keystore: "{% if elasticsearch_ssl_cert_generate %}elasticsearch_cert_files/{{ ansible_hostname }}.p12{% endif %}"
elasticsearch_ssl_keystore_password: ""
elasticsearch_ssl_truststore: "{% if elasticsearch_ssl_cert_generate %}elasticsearch_cert_files/{{ ansible_hostname }}.p12{% endif %}"
elasticsearch_ssl_truststore_password: ""
elasticsearch_ssl_key: ""
elasticsearch_ssl_key_password: ""
elasticsearch_ssl_certificate: ""
elasticsearch_ssl_certificate_authority: ""
elasticsearch_ssl_verification_mode: "full"
```

## 依赖


## github地址
https://github.com/lework/Ansible-roles/tree/master/elasticsearch

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - elasticsearch
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`
```yaml
---

- hosts: node
  vars:
    - elasticsearch_repo_install: false
    - __package_file: elasticsearch-7.8.1-x86_64.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.1-x86_64.rpm
  roles:
  - elasticsearch
```

### 指定配置

```yaml
---

- hosts: 192.168.77.160
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_heap_size: 2g
    - elasticsearch_conf:
        node.name: "node1"
        cluster.name: "custom-cluster"
        discovery.seed_hosts: "localhost:9301"
        http.port: 9201
        transport.port: 9301
        bootstrap.memory_lock: true
  roles:
  - elasticsearch
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - elasticsearch_conf_file: elasticsearch.yml
  roles:
  - elasticsearch
```

### 安装插件

```yaml
---

- hosts: node
  vars:
    - elasticsearch_plugin:
      - ingest-attachment
  roles:
  - elasticsearch
```

### 集群

> 三节点集群

```yaml
---

- hosts: 192.168.77.132,192.168.77.133,192.168.77.134
  vars:
    - ipnames:
        '192.168.77.132': 'es-node1'
        '192.168.77.133': 'es-node2'
        '192.168.77.134': 'es-node3'
  roles:
    - hostnames

- hosts: 192.168.77.132,192.168.77.133,192.168.77.134
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_conf:
        discovery.seed_hosts:
          - '192.168.77.132'
          - '192.168.77.133'
          - '192.168.77.134'
        cluster.initial_master_nodes:
          - 'es-node1'
          - 'es-node2'
          - 'es-node3'
  roles:
  - elasticsearch
```

> 三节点集群, 不同节点角色

```yaml
---

- hosts: 192.168.77.132,192.168.77.133,192.168.77.134
  vars:
    - ipnames:
        '192.168.77.132': 'es-node1'
        '192.168.77.133': 'es-node2'
        '192.168.77.134': 'es-node3'
  roles:
    - hostnames

- hosts: 192.168.77.132
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_conf:
        node.data: false
        node.master: true
        discovery.seed_hosts:
          - '192.168.77.132'
          - '192.168.77.133'
          - '192.168.77.134'
        cluster.initial_master_nodes:
          - 'es-node1'
  roles:
  - elasticsearch

- hosts: 192.168.77.133,192.168.77.134
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_conf:
        node.data: true
        node.master: false
        node.voting_only: false 
        node.ingest: false 
        node.ml: false
        xpack.ml.enabled: false
        node.transform: false
        node.remote_cluster_client: false
        discovery.seed_hosts:
          - '192.168.77.132'
          - '192.168.77.133'
          - '192.168.77.134'
  roles:
  - elasticsearch
```

### 开启xpack

> 单实例, 自动生成tls证书, 也可以指定证书文件，具体变量看角色默认变量

```yaml
---

- hosts: 192.168.77.133
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_xpack_enable: true
    - elasticsearch_enable_http_ssl: true
    - elasticsearch_enable_transport_ssl: true
    - elasticsearch_ssl_cert_generate: true
  roles:
  - elasticsearch
```

> 三节点实例, 自动生成tls证书

```yaml
---

- hosts: 192.168.77.132,192.168.77.133,192.168.77.134
  vars:
    - ipnames:
        '192.168.77.132': 'es-node1'
        '192.168.77.133': 'es-node2'
        '192.168.77.134': 'es-node3'
  roles:
    - hostnames

- hosts: 192.168.77.132,192.168.77.133,192.168.77.134
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_conf:
        discovery.seed_hosts:
          - '192.168.77.132'
          - '192.168.77.133'
          - '192.168.77.134'
        cluster.initial_master_nodes:
          - 'es-node1'
          - 'es-node2'
          - 'es-node3'
    - elasticsearch_xpack_enable: true
    - elasticsearch_enable_http_ssl: true
    - elasticsearch_enable_transport_ssl: true
    - elasticsearch_ssl_cert_generate: true
  roles:
  - elasticsearch
```

> 三节点实例, 不同节点角色，自动生成tls证书

因为需要自动生成tls证书，这里对节点角色的定义放在group_vars变量中。

hosts:
```ini
[es_master]
192.168.77.132 ansible_user=root ansible_password=123456

[es_data]
192.168.77.133 ansible_user=root ansible_password=123456
192.168.77.134 ansible_user=root ansible_password=123456
```


group_vars:
```bash
# tree group_vars/                                
group_vars/
├── es_data.yml
└── es_master.yml

0 directories, 2 files

# cat group_vars/es_master.yml
---

elasticsearch_conf:
  node.data: true
  node.master: false
  node.voting_only: false 
  node.ingest: false 
  node.ml: false
  xpack.ml.enabled: false
  node.transform: false
  node.remote_cluster_client: false
  discovery.seed_hosts:
    - '192.168.77.132'
    - '192.168.77.133'
    - '192.168.77.134'
  cluster.initial_master_nodes:
    - 'es-master'

# cat group_vars/es_data.yml
---

elasticsearch_conf:
  node.data: false
  node.master: true
  discovery.seed_hosts:
    - '192.168.77.132'
    - '192.168.77.133'
    - '192.168.77.134'
  cluster.initial_master_nodes:
    - 'es-master'
```

playbook

```yaml
---

- hosts: es_master,es_data
  vars:
    - ipnames:
        '192.168.77.132': 'es-master'
        '192.168.77.133': 'es-data1'
        '192.168.77.134': 'es-data2'
  roles:
    - hostnames

- hosts: es_master,es_data
  vars:
    - elasticsearch_repo_install: false
    - elasticsearch_xpack_enable: true
    - elasticsearch_enable_http_ssl: true
    - elasticsearch_enable_transport_ssl: true
    - elasticsearch_ssl_cert_generate: true
  roles:
  - elasticsearch
```