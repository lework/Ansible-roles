# Ansible Role: etcd

安装etcd

## 介绍
etcd是一个高可用的键值存储系统，主要用于共享配置和服务发现。etcd是由CoreOS开发并维护的，灵感来自于 ZooKeeper 和 Doozer，它使用Go语言编写，并通过Raft一致性算法处理日志复制以保证强一致性。Raft是一个来自Stanford的新的一致性算法，适用于分布式系统的日志复制，Raft通过选举的方式来实现一致性，在Raft中，任何一个节点都可能成为Leader。Google的容器集群管理系统Kubernetes、开源PaaS平台Cloud Foundry和CoreOS的Fleet都广泛使用了etcd。

官方地址： https://coreos.com/etcd/

github: https://github.com/coreos/etcd

官方文档地址：https://coreos.com/etcd/docs/latest

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

os `Centos 7.4 X64`

python `2.7.5`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    etcd_version: "3.3.2"

    etcd_file: "etcd-v{{ etcd_version }}-linux-amd64.tar.gz"
    etcd_file_path: "{{ software_files_path }}/{{ etcd_file }}"
    etcd_file_url: "https://github.com/coreos/etcd/releases/download/etcd-v{{ etcd_version }}/{{ etcd_file }}"

    etcd_port: 2379
    etcd_peer_port: 2380
    etcd_home: "/etcd_data"
    etcd_datadir: "{{ etcd_home }}/{{ etcd_port }}/data"
    etcd_confdir: "{{ etcd_home }}/{{ etcd_port }}/conf"
    etcd_wardir: "{{ etcd_home }}/{{ etcd_port }}/war"

    etcd_user: "etcd"
    etcd_name: "infra0"
    etcd_service_name: "etcd{% if etcd_port != 2379 %}{{ etcd_port }}{% endif %}"
    etcd_initial_advertise_peer_urls: "http://{{ ansible_default_ipv4.address }}:{{ etcd_peer_port }}"
    etcd_listen_peer_urls: "http://{{ ansible_default_ipv4.address }}:{{ etcd_peer_port }}"
    etcd_listen_client_urls: "http://0.0.0.0:{{ etcd_port }}"
    etcd_advertise_client_urls: "http://{{ ansible_default_ipv4.address }}:{{ etcd_port }}"

    etcd_trusted_ca_file: false
    etcd_cert_file: false
    etcd_key_file: false
    etcd_peer_trusted_ca_file: false
    etcd_peer_cert_file: false
    etcd_peer_key_file: false

    etcd_auto_tls: false

    etcd_discovery: false
    etcd_initial_cluster: false
    etcd_initial_cluster_token: "etcd_cluster_1"

    etcd_proxy: false

    etcd_force_new_cluster: false
    etcd_debug: false
    etcd_gomaxprocs: 1

## 依赖

go

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/etcd

## Example Playbook

    安装etcd，默认端口2379：
    - hosts: node1
      roles:
       - { role: etcd }

    单机伪集群安装：
    - hosts: node1
      vars:
       - etcd_initial_cluster: "infra0=http://192.168.77.129:2380,infra1=http://192.168.77.129:2480,infra2=http://192.168.77.129:2580"
      roles:
       - { role: etcd, etcd_name: "infra0", etcd_port: 2379, etcd_peer_port: 2380}
       - { role: etcd, etcd_name: "infra1", etcd_port: 2479, etcd_peer_port: 2480}
       - { role: etcd, etcd_name: "infra2", etcd_port: 2579, etcd_peer_port: 2580}


    分布式安装：
    端口默认
    - hosts: node4
      vars:
       - etcd_initial_cluster: "infra0=http://192.168.77.133:2380,infra1=http://192.168.77.134:2380,infra2=http://192.168.77.135:2380"
      roles:
       - { role: etcd, etcd_name: "infra0" }
    
    - hosts: node5
      vars:
       - etcd_initial_cluster: "infra0=http://192.168.77.133:2380,infra1=http://192.168.77.134:2380,infra2=http://192.168.77.135:2380"
      roles:
       - { role: etcd, etcd_name: "infra1" }
       
    - hosts: node6
      vars:
       - etcd_initial_cluster: "infra0=http://192.168.77.133:2380,infra1=http://192.168.77.134:2380,infra2=http://192.168.77.135:2380"
      roles:
       - { role: etcd, etcd_name: "infra2" }
    
## 使用
    
启动命令： `systemctl start etcd`