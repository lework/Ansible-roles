# Ansible Role: rabbitmq

安装rabbitmq服务

## 介绍
RabbitMQ是一个在AMQP基础上完成的，可复用的企业消息系统。他遵循Mozilla Public License开源协议。

官方地址：http://www.rabbitmq.com/
官方文档地址：http://www.rabbitmq.com/documentation.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    rabbitmq_version: "3.6.9"

    rabbitmq_file: "rabbitmq-server-generic-unix-{{ rabbitmq_version }}.tar.xz"
    rabbitmq_file_path: "{{ software_files_path }}/{{ rabbitmq_file }}"
    rabbitmq_file_url: "https://www.rabbitmq.com/releases/rabbitmq-server/v{{ rabbitmq_version }}/rabbitmq-server-generic-unix-{{ rabbitmq_version }}.tar.xz"

    rabbitmq_user: rabbitmq
    rabbitmq_nodename: rabbit
    rabbitmq_bindip: 0.0.0.0
    rabbitmq_nodeport: 5672
    rabbitmq_logdir: /var/log/rabbitmq
    rabbitmq_mnesiadir: /rabbitmq_data/mnesia
    rabbitmq_enabled: true

    rabbitmq_plugins: []
    #rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']

    rabbitmq_server_users: []
    #rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
    rabbitmq_vhost: "/"
    rabbitmq_vhost_permission : "'.*' '.*' '.*'"
    rabbitmq_cluster: false
    rabbitmq_policy: "all '^.*' '{\"ha-mode\": \"all\"}'"
    rabbitmq_cluster_ram: false

## 依赖

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/rabbitmq

## Example Playbook
    安装rabbitmq
    - hosts: node1
      vars:
       - rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']
       - rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
      roles:
       - erlang
       - rabbitmq
       
    安装rabbitmq集群，采用镜像策略
    - hosts: node1 node2 node3
      vars:
       - rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']
       - rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
       - 
      roles:
       - erlang
       - rabbitmq

## 使用

rabbitmq-server管理
```
/etc/init.d/rabbitmq-server
Usage: /etc/init.d/rabbitmq-server {start|stop|status|rotate-logs|restart|condrestart|try-restart|reload|force-reload}
```
rabbitmqctl管理
```
关闭app 
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl stop_app'
加入集群
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl join_cluster rabbit@node1'
启动app
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl start_app'
查看集群状态
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl cluster_status'
```