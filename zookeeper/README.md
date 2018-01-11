# Ansible Role: zookeeper

安装zookeeper

## 介绍
ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现，是Hadoop和Hbase的重要组件。它是一个为分布式应用提供一致性服务的软件，提供的功能包括：配置维护、域名服务、分布式同步、组服务等。


官方地址： https://zookeeper.apache.org/
官方文档地址：https://zookeeper.apache.org/doc/trunk/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    zookeeper_version: "3.4.9"

    zookeeper_file: "zookeeper-{{ zookeeper_version }}.tar.gz"
    zookeeper_file_path: "{{ software_files_path }}/{{ zookeeper_file }}"
    zookeeper_file_url: "http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-{{ zookeeper_version }}/zookeeper-{{ zookeeper_version }}.tar.gz"

    zookeeper_user: "zookeeper"
    zookeeper_port: 2181
    zookeeper_name: "zookeeper{{ zookeeper_port if zookeeper_port != 2181 else '' }}" 
    zookeeper_home: "/zookeeper_data"
    zookeeper_dir: "{{ zookeeper_home }}/{{ zookeeper_port }}"
    zookeeper_datadir: "{{ zookeeper_home }}/{{ zookeeper_port }}/data"
    zookeeper_datalogdir: "{{ zookeeper_home }}/{{ zookeeper_port }}/logs"
    zookeeper_hosts:
      - {'host': 127.0.0.1, 'port': 2181 ,'id': 1, 'leader_port': '2888:3888'}
        

## 依赖

java

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/zookeeper

## Example Playbook

    安装zookeeper，默认端口2181：
    - hosts: 192.168.77.129
      roles:
       - { role: zookeeper }

    单机伪集群安装：
    - hosts: 192.168.77.129
      vars:
       - zookeeper_hosts:
          - {'host': 192.168.77.129, 'id': 1, 'port': 2181, 'leader_port': '2888:3888'}
          - {'host': 192.168.77.129, 'id': 2, 'port': 2182, 'leader_port': '2889:3889'}
          - {'host': 192.168.77.129, 'id': 3, 'port': 2183, 'leader_port': '2890:3890'}

      roles:
       - { role: zookeeper, zookeeper_port: 2181 }
       - { role: zookeeper, zookeeper_port: 2182 }
       - { role: zookeeper, zookeeper_port: 2183 }

    分布式安装：
    全部默认
    - hosts: 192.168.77.129 192.168.77.130 192.168.77.131
      vars:
        - zookeeper_hosts: "{{ play_hosts }}"
      roles:
         - { role: zookeeper }
    指定id
    - hosts: 192.168.77.129 192.168.77.130 192.168.77.131
      vars:
       - zookeeper_hosts:
          - {'host': 192.168.77.129, 'id': 1}
          - {'host': 192.168.77.130, 'id': 2}
          - {'host': 192.168.77.131, 'id': 3}

      roles:
       - { role: zookeeper}
    端口自定义
    - hosts: 192.168.77.129 192.168.77.130 192.168.77.131
      vars:
       - zookeeper_hosts:
          - {'host': 192.168.77.129, 'id': 1, 'port': 2182, 'leader_port': '2889:3889'}
          - {'host': 192.168.77.130, 'id': 2, 'port': 2182, 'leader_port': '2889:3889'}
          - {'host': 192.168.77.131, 'id': 3, 'port': 2182, 'leader_port': '2889:3889'}

      roles:
       - { role: zookeeper, zookeeper_port: 2182}

## 使用
/etc/init.d/zookeeper
Usage: /etc/init.d/zookeeper {start|stop|status|sstatus|restart|condrestart}

启动命令：/etc/init.d/zookeeper start 
关闭命令：/etc/init.d/zookeeper stop 
查看状态命令：/etc/init.d/zookeeper sstatus 
客户端命令：zkCli.sh -server localhost:2181 