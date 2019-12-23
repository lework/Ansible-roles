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

os `Centos 7.4 X64` `Debian 7.4 X64`

## 角色变量
```
software_files_path: "/opt/software"
software_install_path: "/usr/local"

rabbitmq_version: "3.8.2"

rabbitmq_file: "rabbitmq-server-generic-unix-{{ rabbitmq_version }}.tar.xz"
rabbitmq_file_path: "{{ software_files_path }}/{{ rabbitmq_file }}"
rabbitmq_file_url: "https://github.com/rabbitmq/rabbitmq-server/releases/download/v{{ rabbitmq_version }}/rabbitmq-server-generic-unix-{{ rabbitmq_version }}.tar.xz"


rabbitmq_user: rabbitmq
rabbitmq_nodename: "rabbit@{{ ansible_hostname }}"
rabbitmq_bindip: 0.0.0.0
rabbitmq_nodeport: 5672
rabbitmq_management_port: 15672

rabbitmq_logdir: /var/log/rabbitmq
rabbitmq_mnesiadir: /var/lib/rabbitmq/mnesia

rabbitmq_vm: 512MiB

rabbitmq_plugins: []
#rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']

rabbitmq_server_users: []
#rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]

rabbitmq_vhost: "/"
rabbitmq_vhost_permission : "'.*' '.*' '.*'"

rabbitmq_policy: 
 - "all '^.*' '{\"ha-mode\": \"all\"}'"

rabbitmq_cluster: false
rabbitmq_cluster_ram: false
rabbitmq_cluster_name: rabbitmq-cluster

rabbitmq_cluster_discovery_classic: false

rabbitmq_cookie: "rabbitmq-{% if rabbitmq_cluster %}cluster{% else %}sigle{% endif %}"
```

## 依赖

- `hostnames` role
- `erlang` role

## github地址

https://github.com/lework/Ansible-roles/tree/master/rabbitmq

## Example Playbook
```yaml
# 单实例安装rabbitmq
---
- hosts: 192.168.77.130
  roles:
   - erlang
   - rabbitmq

# 单实例安装rabbitmq, 并指定版本和启用插件和添加用户
- hosts: node1
  vars:
   - rabbitmq_version: "3.7.23"
   - rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']
   - rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
  roles:
   - erlang
   - rabbitmq
   
# 集群安装rabbitmq, 采用镜像策略
---
- hosts: 192.168.77.130 192.168.77.131 192.168.77.132
  vars:
   - ipnames:
       '192.168.77.130': 'node1'
       '192.168.77.131': 'node2'
       '192.168.77.132': 'node3'
   - rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']
   - rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
   - rabbitmq_cluster: true
  roles:
   - hostnames
   - erlang
   - rabbitmq

# 集群安装rabbitmq, 采用镜像策略, 使用静态集群配置
---
- hosts: 192.168.77.140 192.168.77.141 192.168.77.142
  vars:
   - ipnames:
       '192.168.77.140': 'node1'
       '192.168.77.141': 'node2'
       '192.168.77.142': 'node3'
   - rabbitmq_plugins: ['rabbitmq_top', 'rabbitmq_mqtt']
   - rabbitmq_server_users: [{user: 'test', pass: '123456', role: 'administrator'}]
   - rabbitmq_cluster: true
   - rabbitmq_cluster_discovery_classic: true
  roles:
   - hostnames
   - erlang
   - rabbitmq
```

## 使用

rabbitmq-server管理

```
systemctl status rabbimq-server
systemctl stop rabbimq-server
systemctl start rabbimq-server
```

rabbitmqctl管理

```
# 关闭app 
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl stop_app'
# 加入集群
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl join_cluster rabbit@node1'
# 启动app
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl start_app'
# 查看集群状态
su -l rabbitmq -s /bin/sh -c 'rabbitmqctl cluster_status'
```