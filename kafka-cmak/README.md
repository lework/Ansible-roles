# Ansible Role: cmak

安装cmak服务

## 介绍
cmak（以前称为Kafka Manager） 是 Yahoo 推出的 Kafka 管理工具，支持：

- 管理多个集群
- 轻松检查集群状态 (topics, brokers, replica distribution, partition distribution)
- 执行复制选举
- 生成分区指派，基于集群的状态
- 分区的重新指派

该项目基于 Play Framework 框架开发。

github: https://github.com/yahoo/cmak

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

kafka_cmak_version: "3.0.0.5"

kafka_cmak_file: "cmak-{{ kafka_cmak_version }}.zip"
kafka_cmak_file_path: "{{ software_files_path }}/{{ kafka_cmak_file }}"
kafka_cmak_file_url: "https://github.com/yahoo/CMAK/releases/download/{{ kafka_cmak_version }}/{{ kafka_cmak_file }}"

# User
kafka_cmak_user: "kafka"
kafka_cmak_group: "kafka"

# Port
kafka_cmak_port: 9000

# Path
kafka_cmak_home: "{{ software_install_path }}/cmak"

# Service
kafka_cmak_service_name: "kafka-cmak" 
kafka_cmak_service_status: started
kafka_cmak_service_enabled: yes


# Config
kafka_cmak_zk_hosts: 'localhost:2181'
kafka_cmak_auth_enable: true
kafka_cmak_auth_user: "admin"
kafka_cmak_auth_pass: "admin"

kafka_cmak_javahome: ""
```

## 依赖

- openjdk
- zookeeper

## github地址

https://github.com/lework/Ansible-roles/tree/master/kafka-cmak

## Example Playbook

### 默认安装

```yaml
---

- hosts: 192.168.77.130
  vars:
   - openjdk_packages: java-11-openjdk
  roles:
    - openjdk
    - kafka-cmak
```

### 自定义参数

```yaml
---

- hosts: 192.168.77.130
  vars:
   - kafka_cmak_port: 8080
   - kafka_cmak_zk_hosts: 'localhost:2181'
   - kafka_cmak_auth_enable: true
   - kafka_cmak_auth_user: "admin"
   - kafka_cmak_auth_pass: "admin"
   - kafka_cmak_javahome: "/usr/lib/jvm/zulu-11-amd64"
  roles:
    - kafka-cmak
```
