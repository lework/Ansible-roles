# Ansible Role: elasticsearch

安装elasticsearch集群

## 介绍

ElasticSearch是一个基于Lucene的搜索服务器。它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是当前流行的企业级搜索引擎。设计用于云计算中，能够达到实时搜索，稳定，可靠，快速，安装使用方便。

官方地址： https://www.elastic.co/products/elasticsearch
github: https://github.com/elastic/elasticsearch
官方文档地址：https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    es_version: "5.4.1"

    es_file: "elasticsearch-{{ es_version }}.tar.gz"
    es_file_path: "{{ software_files_path }}/{{ es_file }}"
    es_file_url: "https://artifacts.elastic.co/downloads/elasticsearch/{{ es_file }}"

    es_user: elasticsearch
    es_group: elasticsearch

    es_http_host: "0.0.0.0"
    es_http_port: 9200
    es_transport_port: 9300

    es_max_open_files: 165535
    es_max_map_count: 262155
    es_max_processes: 4096

    es_service_name: "elasticsearch{% if es_http_port != 9200 %}{{ es_http_port }}{% endif %}"
    es_service_start: false

    es_home_dir: "/usr/local/elasticsearch"
    es_pid_dir: "/var/run/elasticsearch"
    es_log_dir: "/{{ es_service_name }}_data/logs"
    es_conf_dir: "/{{ es_service_name }}_data/config"
    es_data_dir: "/{{ es_service_name }}_data/data"
    es_script_dir: "/{{ es_service_name }}_data/scripts"

    es_cluster_name: ""
    es_node_name: ""
    es_node_rack: ""

    es_unicast_hosts: ""
    es_minimum_master_nodes: ""

    es_scripts_fileglob: ""
    es_install_plugins: []
    es_config: ""

    es_heap_ms: "1g"
    es_heap_mx: "1g"
    es_jvm_options: ""
    es_java_home: ""
    es_g1gc: false

    es_node_data: false
    es_node_master: false
    es_node_ingest: false
    es_node_client: false
    
## 依赖

java 1.8

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/elasticsearch

## Example Playbook

    #单机单实例,默认配置
    - hosts: node1
      roles:
        - { role: java ,java_version: "1.8" }
        - role: elasticsearch
       

    #单机多实例
    - hosts: node1
      vars:
       - es_cluster_name: "Testes"
         es_unicast_hosts: '["192.168.77.129:9301","192.168.77.129:9302"]'
         es_minimum_master_nodes: 2
         es_heap_ms: "512m"
         es_heap_mx: "512m"
      roles:
       - { role: java ,java_version: "1.8" }
       - { role: elasticsearch, es_http_port: 9201, es_transport_port: 9301, es_node_name: "es_node1" }
       - { role: elasticsearch, es_http_port: 9202, es_transport_port: 9302, es_node_name: "es_node2" }
    
    #自定义节点角色
    - hosts: node1
      vars:
       - es_cluster_name: "Testes"
         es_unicast_hosts: '["192.168.77.129:9301","192.168.77.129:9302","192.168.77.129:9303"]'
         es_minimum_master_nodes: 1
         es_heap_ms: "512m"
         es_heap_mx: "512m"
         es_install_plugins:
           - x-pack
           - ingest-geoip
         es_service_start: true
      roles:
       - { role: java ,java_version: "1.8" }
       - { role: elasticsearch, es_http_port: 9201, es_transport_port: 9301, es_node_name: "es_node1", es_node_master: true, es_node_ingest: true }
       - { role: elasticsearch, es_http_port: 9202, es_transport_port: 9302, es_node_name: "es_node2", es_node_data: true }
       - { role: elasticsearch, es_http_port: 9203, es_transport_port: 9303, es_node_name: "es_node3", es_node_data: true }
    
    #分布式部署
    - hosts: node1 node2 node3
      vars:
       - es_cluster_name: "Testes"
         es_unicast_hosts: '["192.168.77.129","192.168.77.130","192.168.77.131"]'
         es_minimum_master_nodes: 2
         es_heap_ms: "512m"
         es_heap_mx: "512m"
       - es_install_plugins:
           - x-pack
           - ingest-geoip
         es_service_start: true
      roles:
       - { role: java ,java_version: "1.8" }
       - { role: elasticsearch }


## 使用

```
~]# service elasticsearch
Usage: /etc/init.d/elasticsearch {start|stop|status|restart|condrestart|try-restart|reload|force-reload}
```