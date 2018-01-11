# Ansible Role: Kafka Manager

安装Kafka Manager服务

## 介绍
Kafka Manager 是 Yahoo 推出的 Kafka 管理工具，支持：

- 管理多个集群
- 轻松检查集群状态 (topics, brokers, replica distribution, partition distribution)
- 执行复制选举
- 生成分区指派，基于集群的状态
- 分区的重新指派

该项目基于 Play Framework 框架开发。

github: https://github.com/yahoo/kafka-manager

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    kafka_manager_version: "1.3.3.6"

    kafka_manager_file: "kafka-manager-{{ kafka_manager_version }}.tar.gz"
    kafka_manager_file_path: "{{ software_files_path }}/{{ kafka_manager_file }}"
    kafka_manager_file_url: "https://github.com/yahoo/kafka-manager/archive/{{ kafka_manager_version }}.tar.gz"

    kafka_manager_build_file: "kafka-manager-{{ kafka_manager_version }}.zip"
    kafka_manager_build_file_path: "{{ software_files_path }}/{{ kafka_manager_build_file }}"

    kafka_manager_user: "kafka-manager"
    kafka_manager_port: 9000

    kafka_manager_zk: 'localhost:2181'
    kafka_manager_auth: false
    kafka_manager_auth_user: "admin"
    kafka_manager_auth_pass: "password"

    kafka_manager_javahome: ""

## 依赖
Kafka 0.8.1.1 or 0.8.2.* or 0.9.0.* or 0.10.0.*
Java 8+
sbt

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/kafka-manager

## Example Playbook
    - hosts: node1 
      roles:
        - kafka-manager

    自定义参数
    - hosts: node1
      vars:
        - kafka_manager_javahome: " /usr/java/jdk1.8.0_121"
        - kafka_manager_zk: "node1:2181,node2:2181,node3:2181"
        - kafka_manager_port: "8080"
      roles:
        - { role: kafka-manager }
## 使用
service kafka-manager 
Usage: /etc/init.d/kafka-manager {start|stop|status|restart|reload|force-reload|condrestart}
