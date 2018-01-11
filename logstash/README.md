# Ansible Role: logstash

安装logstash

## 介绍
Logstash 是一个应用程序日志、事件的传输、处理、管理和搜索的平台。你可以用它来统一对应用程序日志进行收集管理，提供 Web 接口用于查询和统计。

官方地址： https://www.elastic.co/products/logstash
github: https://github.com/elastic/logstash
官方文档地址：https://www.elastic.co/guide/en/logstash/current/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    logstash_version: "5.4.1"

    logstash_file: "logstash-{{ logstash_version }}.tar.gz"
    logstash_file_path: "{{ software_files_path }}/{{ logstash_file }}"
    logstash_file_url: "https://artifacts.elastic.co/downloads/logstash/{{ logstash_file }}"

    logstash_user: logstash
    logstash_group: logstash

    logstash_home_dir: "/usr/local/logstash"
    logstash_log_dir: "/var/log/logstash"
    logstash_pid_dir: "/var/run/logstash"
    logstash_conf_dir: "{{ logstash_home_dir }}/config"
    logstash_data_dir: "{{ logstash_home_dir }}/data"
    logstash_pipeline_dir: "{{ logstash_home_dir }}/pipeline"
    logstash_pipeline_file: "{{ logstash_service_name }}.conf"

    logstash_node_name: ""
    logstash_service_name: "logstash"
    logstash_service_start: false

    logstash_install_plugins: []
    logstash_config: ""

    logstash_heap_ms: "256m"
    logstash_heap_mx: "1g"
    logstash_jvm_options: ""
    logstash_java_home: ""

## 依赖

java 1.8

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/logstash

## Example Playbook

    #单机单实例
    - hosts: node1
      vars:
      - logstash_config: |
          'input {
            beats {
            port => 5045
            codec => multiline{
              pattern => "^^# User@Host:"
              negate => true
              what => previous
            }
            }
          }
          filter {
            grok {
            match => [ "message", "^# User@Host: %{USER:user}(?>\[[^\]]+\])? @ (%{HOSTNAME:hostname})? \[%{IP:ip}?\](\s+)Id:(\s+)%{INT:id:int}(\n)?# Query_time: %{NUMBER:query_time:float}\s+Lock_time: %{NUMBER:lock_time:scaled_float}\s+Rows_sent: %{NUMBER:rows_sent:int}\s+Rows_examined: %{NUMBER:rows_examined:int}(\n)?(?:use %{DATA:database};\s*)?(\n)?SET timestamp=%{NUMBER:timestamp};(\n)?(?<query>(?<action>\w+)(\s+.*)?)?;(\n# Time: .*$)?" ]
            }
            date {
            match => [ "timestamp", "UNIX" ]
            remove_field => [ "timestamp" ]
            }
            mutate {
            lowercase => ["action"]
            }
          }
          output {
            stdout { codec => rubydebug }
          }'
      - logstash_heap_mx: "256m"
        logstash_service_start: true
      roles:
       - { role: logstash }
   
    #单机多实例
    - hosts: node1
      vars:
      - logstash_config_1: |
          'input {
            beats {
            port => 5044
            codec => multiline{
              pattern => "^^# User@Host:"
              negate => true
              what => previous
            }
            }
          }
          filter {
            grok {
            match => [ "message", "^# User@Host: %{USER:user}(?>\[[^\]]+\])? @ (%{HOSTNAME:hostname})? \[%{IP:ip}?\](\s+)Id:(\s+)%{INT:id:int}(\n)?# Query_time: %{NUMBER:query_time:float}\s+Lock_time: %{NUMBER:lock_time:scaled_float}\s+Rows_sent: %{NUMBER:rows_sent:int}\s+Rows_examined: %{NUMBER:rows_examined:int}(\n)?(?:use %{DATA:database};\s*)?(\n)?SET timestamp=%{NUMBER:timestamp};(\n)?(?<query>(?<action>\w+)(\s+.*)?)?;(\n# Time: .*$)?" ]
            }
            date {
            match => [ "timestamp", "UNIX" ]
            remove_field => [ "timestamp" ]
            }
            mutate {
            lowercase => ["action"]
            }
          }
          output {
            stdout { codec => rubydebug }
          }'
      - logstash_config_2: |
          'input {
            beats {
            port => 5045
            codec => multiline{
              pattern => "^^# User@Host:"
              negate => true
              what => previous
            }
            }
          }
          filter {
            grok {
            match => [ "message", "^# User@Host: %{USER:user}(?>\[[^\]]+\])? @ (%{HOSTNAME:hostname})? \[%{IP:ip}?\](\s+)Id:(\s+)%{INT:id:int}(\n)?# Query_time: %{NUMBER:query_time:float}\s+Lock_time: %{NUMBER:lock_time:scaled_float}\s+Rows_sent: %{NUMBER:rows_sent:int}\s+Rows_examined: %{NUMBER:rows_examined:int}(\n)?(?:use %{DATA:database};\s*)?(\n)?SET timestamp=%{NUMBER:timestamp};(\n)?(?<query>(?<action>\w+)(\s+.*)?)?;(\n# Time: .*$)?" ]
            }
            date {
            match => [ "timestamp", "UNIX" ]
            remove_field => [ "timestamp" ]
            }
            mutate {
            lowercase => ["action"]
            }
          }
          output {
            stdout { codec => rubydebug }
          }'
      - logstash_heap_mx: "256m"
        logstash_service_start: true
      roles:
       - { role: logstash, logstash_service_name: logstash-mysqlslow, logstash_config: "{{logstash_config_1}}"}
       - { role: logstash, logstash_service_name: logstash-mysqlslow2, logstash_config: "{{logstash_config_2}}"}

## 使用

```
service logstash-mysqlslow
Usage:  {start|stop|force-stop|status|restart}
```
