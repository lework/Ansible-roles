# Ansible Role: kibana

安装kibana

## 介绍

Kibana 是一个为 Logstash 和 ElasticSearch 提供的日志分析的 Web 接口。可使用它对日志进行高效的搜索、可视化、分析等各种操作。

官方地址： https://www.elastic.co/products/kibana
github: https://github.com/elastic/kibana
官方文档地址：https://www.elastic.co/guide/en/kibana/current/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    kibana_version: "5.4.1"

    kibana_file: "kibana-{{ kibana_version }}-linux-x86_64.tar.gz"
    kibana_file_path: "{{ software_files_path }}/{{ kibana_file }}"
    kibana_file_url: "https://artifacts.elastic.co/downloads/kibana/{{ kibana_file }}"

    kibana_user: kibana
    kibana_group: kibana

    kibana_home_dir: "/usr/local/kibana"
    kibana_log_dir: "/var/log/kibana"
    kibana_pid_dir: "/var/run/kibana"
    kibana_conf_dir: "{{ kibana_home_dir }}/config"
    kibana_data_dir: "{{ kibana_home_dir }}/data"

    kibana_service_name: "kibana"
    kibana_service_start: false
    kibana_conf_file: "{{ kibana_service_name }}.yml"

    kibana_server_port: "5601"
    kibana_server_host: "0.0.0.0"

    kibana_elasticsearch_url: ""
    kibana_elasticsearch_username: ""
    kibana_elasticsearch_password: ""
    kibana_elasticsearch_pingTimeout: ""
    kibana_elasticsearch_requestTimeout: ""
    kibana_elasticsearch_startupTimeout: ""

    kibana_tilemap_gaode: true

    kibana_install_plugins: []
    kibana_config: {}

## 依赖

elasticsearch

## github地址

https://github.com/kuailemy123/Ansible-roles/tree/master/kibana

## Example Playbook

    - hosts: node1
      vars:
       - kibana_elasticsearch_url: "http://localhost:9200"
         kibana_elasticsearch_username: "kibana"
         kibana_elasticsearch_password: "123456"
         kibana_install_plugins:
           - "x-pack"
         kibana_service_start: true
      roles:
       - kibana

## 使用

```
service kibana
Usage:  {start|stop|force-stop|status|restart}
```