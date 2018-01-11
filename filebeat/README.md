# Ansible Role: filebeat

安装filebeat，用于收集日志

## 介绍
filebeat最初是基于logstash-forwarder源码的日志数据shipper。Filebeat安装在服务器上作为代理来监视日志目录或特定的日志文件，可以将日志转发到Logstash进行解析，也可以直接发送到Elasticsearch进行索引。

官方地址： https://www.elastic.co/products/beats/filebeat
github: https://github.com/elastic/beats
官方文档地址：https://www.elastic.co/guide/en/beats/filebeat/current/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    filebeat_version: "5.4.1"

    filebeat_file: "filebeat-{{ filebeat_version }}-linux-x86_64.tar.gz"
    filebeat_file_path: "{{ software_files_path }}/{{ filebeat_file }}"
    filebeat_file_url: "https://artifacts.elastic.co/downloads/beats/filebeat/{{ filebeat_file }}"

    filebeat_pid_dir: "/var/run/filebeat"
    filebeat_home_dir: "/usr/local/filebeat"
    filebeat_log_dir: "/var/log/filebeat"
    filebeat_conf_dir: "{{ filebeat_home_dir }}/conf"
    filebeat_data_dir: "{{ filebeat_home_dir }}/data"

    filebeat_service_name: "filebeat"
    filebeat_service_start: false
    filebeat_conf_file: "{{ filebeat_service_name }}.yml"
    filebeat_config : ""

## 依赖

None

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/filebeat

## Example Playbook

    #安装filebeat,监听mysql慢日志：
    - hosts: node1
      vars:
       - filebeat_config: |
           'filebeat.prospectors:
             - input_type: log
               paths:
                 - /var/log/mysql/mysql-slow.log.20170301
               document_type: mysql-slow
               tail_file: false
           output.logstash:
             hosts: ["localhost:5044"]
           processors:
             - drop_fields:
                 fields: ["input_type", "beat", "offset", "source"] 
           logging.to_files: true
           logging.files:
             path: /var/log/filebeat
             name: filebeat-mysql-slow
             rotateeverybytes: 104857600
             keepfiles: 7'
       - filebeat_service_start: true
      roles:
       - filebeat
       
      #多实例部署
      - hosts: node1
        vars:
         - filebeat_config_1: |
            'filebeat.prospectors:
               - input_type: log
                 paths:
                   - /var/log/mysql/mysql-slow.log.20170301
                 document_type: mysql-slow
                 tail_file: false
             output.logstash:
               hosts: ["localhost:5044"]
             processors:
               - drop_fields:
                 fields: ["input_type", "beat", "offset", "source"] 
             logging.to_files: true
             logging.files:
               path: /var/log/filebeat
               name: filebeat-mysql-slow
               rotateeverybytes: 104857600
               keepfiles: 7'
         - filebeat_config_2: |
            'filebeat.prospectors:
               - input_type: log
                 paths:
                   - /var/log/nginx/access.log*
                 document_type: nginx
                 tail_files: true
                 json.keys_under_root: true
                 json.add_error_key: true
             output.logstash:
             hosts: ["localhost:5044"]

             processors:
               - drop_fields:
                 fields: ["input_type", "beat", "offset", "source"] 
             logging.to_files: true
             logging.files:
               path: /var/log/filebeat-nginx
               name: filebeat
               rotateeverybytes: 104857600
               keepfiles: 7'
         - filebeat_service_start: true
        roles:
         - { role: filebeat, filebeat_config: "{{filebeat_config_1}}", filebeat_service_name: "filebeat-mysqlslow" }
         - { role: filebeat, filebeat_config: "{{filebeat_config_2}}", filebeat_service_name: "filebeat-nginx" }



## 使用

```
service filebeat-nginx
Usage: /etc/init.d/filebeat-nginx {start|stop|status|restart|condrestart}
```