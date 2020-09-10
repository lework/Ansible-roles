# Ansible Role: kafka

安装kafka

## 介绍
Kafka是最初由Linkedin公司开发，是一个分布式、分区的、多副本的、多订阅者，基于zookeeper协调的分布式日志系统（也可以当做MQ系统），常见可以用于web/nginx日志、访问日志，消息服务等等，Linkedin于2010年贡献给了Apache基金会并成为顶级开源项目。

官方地址: https://kafka.apache.org/
github: https://github.com/apache/kafka
官方文档地址：https://kafka.apache.org/documentation

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量

```yaml
software_files_path: "/opt/software"
software_install_path: "/usr/local"

kafka_version: "2.6.0"
kafka_scala_version: "2.13"

kafka_file: "kafka_{{ kafka_scala_version }}-{{ kafka_version }}.tgz"
kafka_file_path: "{{ software_files_path }}/{{ kafka_file }}"
kafka_file_url: "https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/{{ kafka_version }}/{{ kafka_file }}"

# Owner
kafka_user: kafka
kafka_group: kafka

# Port
kafka_port: 9092

# Service
kafka_service_name: "kafka{{ '-' ~ kafka_port if kafka_port != 9092 else '' }}" 
kafka_service_status: started
kafka_service_enabled: yes

# Path
kafka_home: "{{ software_install_path }}/kafka"

kafka_data_home: "/data"
kafka_conf_path: "{{ kafka_data_home }}/{{ kafka_service_name }}/config"
kafka_data_path: "{{ kafka_data_home }}/{{ kafka_service_name }}/data"
kafka_log_path: "{{ kafka_data_home }}/{{ kafka_service_name }}/logs"

# Config
kafka_broker_id: "{% for i in ansible_play_hosts_all %}{% if i == inventory_hostname %}{{ loop.index }}{% endif %}{% endfor %}"
kafka_broker_rack: dc1
kafka_listeners: "PLAINTEXT://:{{ kafka_port }}"
kafka_advertised_listeners: "PLAINTEXT://{{ ansible_default_ipv4.address | d(ansible_nodename)}}:{{ kafka_port }}"
kafka_config_extra: ""

# Java options
kafka_heap_opts: "-Xmx1G -Xms1G"
kafka_jmx_enabled: false
kafka_jmx_port: 1099

# zookeeper
kafka_standalone: false
kafka_zookeeper_hosts: "localhost:2181/kafka"
```

## 依赖

- openjdk
- zookeeper

## github地址

https://github.com/lework/Ansible-roles/tree/master/kafka

## Example Playbook

### 默认安装

> 默认端口9092

```yaml
---

- hosts: 192.168.77.129
  vars:
   - openjdk_packages: java-1.8.0-openjdk
  roles:
   - openjdk
   - zookeeper
   - kafka
```

### 单机伪集群安装

```yaml
---
- hosts: 192.168.77.129
  vars:
   - openjdk_packages: java-1.8.0-openjdk
  roles:
   - openjdk
   - zookeeper
   - { role: kafka, kafka_port: 9093, kafka_broker_id: 1 }
   - { role: kafka, kafka_port: 9094, kafka_broker_id: 2 }
   - { role: kafka, kafka_port: 9095, kafka_broker_id: 3 }
```

### Standalone安装

> 这种方式下，不需要单独安装zookeeper，使用kafka自带的。

单点
```yaml
---

- hosts: 192.168.77.129
  vars:
   - kafka_standalone: true
   - openjdk_packages: java-1.8.0-openjdk
  roles:
   - openjdk
   - kafka
```


伪集群
```yaml
---

- hosts: 192.168.77.129
  vars:
   - openjdk_packages: java-1.8.0-openjdk
  roles:
   - openjdk
   - { role: kafka, kafka_port: 9093, kafka_broker_id: 1, kafka_standalone: true }
   - { role: kafka, kafka_port: 9094, kafka_broker_id: 2 }
   - { role: kafka, kafka_port: 9095, kafka_broker_id: 3 }
```

### 分布式集群安装

> zookeeper_hosts 为zookeeper集群主机的列表
> kafka_zookeeper_hosts 为连接zookeeper集群的地址

```yaml
---

- hosts: 192.168.77.130 192.168.77.131 192.168.77.132
  vars:
    - zookeeper_hosts: "{{ ansible_play_hosts_all }}"
    - kafka_zookeeper_hosts: 192.168.77.130:2181,192.168.77.131:2181,192.168.77.132:2181/kafka
  roles:
   - openjdk
   - zookeeper
   - kafka
```

## 使用

非systemd
```bash
/etc/init.d/kafka
Usage: /etc/init.d/kafka {start|stop|status|restart|reload|force-reload|condrestart}

启动命令：/etc/init.d/kafka start 
关闭命令：/etc/init.d/kafka stop 
查看状态命令：/etc/init.d/kafka status
```

systemd
```bash
启动命令：systemctl start kafka
关闭命令：systemctl stop kafka
```