# Ansible Role: Mongodb
安装Mongodb

## 介绍
MongoDB是一个基于分布式文件存储的数据库。由C++语言编写。旨在为WEB应用提供可扩展的高性能数据存储解决方案。
在高负载的情况下，添加更多的节点，可以保证服务器性能。
MongoDB 旨在为WEB应用提供可扩展的高性能数据存储解决方案。
MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。

官方网站：https://www.mongodb.com/
官方文档地址：https://docs.mongodb.com/manual/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    mongodb_version: "3.2.4"

    mongodb_file: "mongodb-linux-x86_64-rhel62-{{ mongodb_version }}.tgz"
    mongodb_file_path: "{{ software_files_path }}/{{ mongodb_file }}"
    mongodb_file_url: "http://downloads.mongodb.org/linux/mongodb-linux-x86_64-rhel62-{{ mongodb_version }}.tgz"

    mongodb_data_path: "/mongodb_data"
    #mongodb_port: 27017
    mongodb_daemon: "mongodb{{ mongodb_port | default('') }}"
    mongodb_dir_path: "{{ mongodb_data_path }}/{{mongodb_port | default('27017') }}"
    mongodb_conf: "{{ mongodb_dir_path }}/mongod.conf"
    mongodb_user: "mongodb"

    mongodb_dbpath: "{{ mongodb_dir_path }}/data"
    mongodb_logpath: "{{ mongodb_dir_path }}/logs/mongod.log"
    mongodb_pidfilepath: "{{ mongodb_dir_path }}/mongod.pid"
    mongodb_fork: true
    mongodb_logappend: true
    mongodb_directoryperdb: true
    mongodb_auth: false
    mongodb_rest: false

    # 主从架构配置
    mongodb_master: false

    mongodb_slave: false
    mongodb_master_source: ''

    # 副本集配置
    mongodb_replSet: false
    mongodb_replSet_exec: false
    mongodb_members: {}

## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/mongodb

## Example Playbook

    安装单个mongodb, 默认端口27017
    - hosts: node1
      roles:
       - { role: mongodb}

    指定端口号，并开启web
    - hosts: node1
      roles:
       - { role: mongodb, mongodb_port: 27018, mongodb_rest: true}

    主从同步
    - hosts: node1
      roles:
       - { role: mongodb, mongodb_port: 27020, mongodb_master: true}
       - { role: mongodb, mongodb_port: 27021, mongodb_slave: true, mongodb_master_source: '192.168.77.129:27020'}

    安装集群
    - hosts: node1
      vars:
        - mongodb_replSet: 'test_rep'
        - mongodb_members: { '0': "192.168.77.129:27031", '1': "192.168.77.129:27032" }
      roles:
        - { role: mongodb, mongodb_port: 27031}
        - { role: mongodb, mongodb_port: 27032, mongodb_replSet_exec: true}
