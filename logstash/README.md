# Ansible Role: logstash

安装logstash

## 介绍
Logstash 是一个应用程序日志、事件的传输、处理、管理和搜索的平台。你可以用它来统一对应用程序日志进行收集管理，提供 Web 接口用于查询和统计。

- 官方地址： https://www.elastic.co/products/logstash
- github: https://github.com/elastic/logstash
- 官方文档地址：https://www.elastic.co/guide/en/logstash/current/index.html

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

logstash_version: "7.8.0"

logstash_service_status: started
logstash_service_enabled: yes

logstash_repo_install: true

logstash_conf_path: /etc/logstash/

logstash_conf:
  pipeline.ordered: auto
  http.enabled: true
  http.host: 0.0.0.0
  http.port: 9600-9700
  path.data: /var/lib/logstash
  path.logs: /var/log/logstash

logstash_conf_file: ""

logstash_pipeline_conf:
   - pipeline.id: main
     path.config: "/etc/logstash/conf.d/*.conf"  

logstash_pipeline: []
logstash_pipeline_file: []

logstash_jvm_heapsize: "1g"

logstash_plugin: []
logstash_plugin_file: []
```

## 依赖

- openjdk

## github地址
https://github.com/lework/Ansible-roles/tree/master/logstash

## Example Playbook

> 默认使用repo方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - openjdk
  - logstash
```

### 使用package包安装

> 默认是安装 `7.8.1` 版本文件，指定版本需指定 `__package_file` 和 `__package_file_url`
```yaml
---

- hosts: node
  vars:
    - logstash_repo_install: false
    - __package_file: logstash-7.8.1.rpm
    - __package_file_url: https://artifacts.elastic.co/downloads/logstash/logstash-7.8.1.rpm
  roles:
  - openjdk
  - logstash
```

### 指定配置

```yaml
---

- hosts: 192.168.77.160
  vars:
    - logstash_repo_install: false
    - logstash_pipeline:
      - name: nginx
        conf: |
         input {
           redis {
             data_type =>"list"
             key =>"nginx_logs"
             host =>"127.0.0.1"
             port => 6379
             password => "pass"
             db => 0
           }
         }
         
         filter {
           geoip {
             target => "geoip"
             source => "client_ip"
             database => "/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-filter-geoip-6.0.3-java/vendor/GeoLite2-City.mmdb"
             add_field => [ "[geoip][coordinates]", "%{[geoip][longitude]}" ]
             add_field => [ "[geoip][coordinates]", "%{[geoip][latitude]}" ]
             remove_field => ["[geoip][latitude]", "[geoip][longitude]", "[geoip][country_code]", "[geoip][country_code2]", "[geoip][country_code3]", "[geoip][timezone]", "[geoip][continent_code]", "[geoip][region_code]"]
           }
           mutate {
             convert => [ "size", "integer" ]
             convert => [ "status", "integer" ]
             convert => [ "request_time", "float" ]
             convert => [ "upstream_response_time", "float" ]
             convert => [ "upstream_connect_time", "float" ]
             convert => [ "[geoip][coordinates]", "float" ]
             remove_field => [ "ecs","agent","host","cloud","@version","input","logs_type" ]
           }
           useragent {
             source => "http_user_agent"
             target => "ua"
             remove_field => [ "[ua][minor]","[ua][major]","[ua][build]","[ua][patch]","[ua][os_minor]","[ua][os_major]" ]
           }
         }
         output {
           elasticsearch {
             hosts => ["http://elastic:9200"]
             user => "elastic"
             password => "pass"
             index => "logstash-nginx-%{+YYYY.MM.dd}"
           }
         } 
  roles:
  - openjdk
  - logstash
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - logstash_conf_file: logstash-conf.yml
    - logstash_pipeline_file:
      - nginx_log.conf
      - http_log.conf
  roles:
  - openjdk
  - logstash
```

### 安装插件

```yaml
---

- hosts: node
  vars:
    - logstash_plugin:
      - logstash-filter-translate
    - logstash_plugin_file:
      - "/tmp/logstash-input-mypluginname-0.1.0.zip"
  roles:
  - openjdk
  - logstash
```
