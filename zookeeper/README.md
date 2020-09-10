# Ansible Role: zookeeper

安装zookeeper

## 介绍
ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现，是Hadoop和Hbase的重要组件。它是一个为分布式应用提供一致性服务的软件，提供的功能包括：配置维护、域名服务、分布式同步、组服务等。


官方地址： https://zookeeper.apache.org/
官方文档地址：https://zookeeper.apache.org/doc/trunk/index.html

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

zookeeper_version: "3.6.1"

zookeeper_file: "apache-zookeeper-{{ zookeeper_version }}-bin.tar.gz"
zookeeper_file_path: "{{ software_files_path }}/{{ zookeeper_file }}"
zookeeper_file_url: "https://mirrors.tuna.tsinghua.edu.cn/apache/zookeeper/zookeeper-{{ zookeeper_version }}/{{ zookeeper_file }}"

# Owner
zookeeper_user: zookeeper
zookeeper_group: zookeeper

# Port
zookeeper_client_port: 2181
zookeeper_connect_port: 2888
zookeeper_elect_port: 3888

# Service
zookeeper_service_name: "zookeeper{{ '-' ~ zookeeper_client_port if zookeeper_client_port != 2181 else '' }}" 
zookeeper_service_status: started
zookeeper_service_enabled: yes

# Path
zookeeper_home: "/data"
zookeeper_conf_path: "{{ zookeeper_home }}/{{ zookeeper_service_name }}"
zookeeper_data_path: "{{ zookeeper_home }}/{{ zookeeper_service_name }}/data"
zookeeper_log_path: "{{ zookeeper_home }}/{{ zookeeper_service_name }}/logs"
zookeeper_data_log_path: "{{ zookeeper_log_path }}"

# Config
zookeeper_init_limit: 10
zookeeper_sync_limit: 5
zookeeper_tick_time: 2000
zookeeper_max_client_connections: 0
zookeeper_autopurge_purge_interval: 1
zookeeper_autopurge_snap_retain_count: 10
zookeeper_admin_enable: false
zookeeper_config_extra: ""

# Java options
zookeeper_server_heap: 1000
zookeeper_client_heap: 256

zookeeper_jmx_enabled: false
zookeeper_jmx_port: 1099
zookeeper_jmx_local_only: 'false'
zookeeper_jmx_auth: 'false'
zookeeper_jmx_ssl: 'false'
zookeeper_jmx_log_disable: 'true'

zookeeper_jvm_opts: "-Djava.net.preferIPv4Stack=true"

# Cluster
zookeeper_hosts: []
#  - {'host': 127.0.0.1, 'port': 2181 ,'id': 1, 'leader_port': '2888:3888'}
```

## 依赖

- openjdk

## github地址
https://github.com/lework/Ansible-roles/tree/master/zookeeper

## Example Playbook

### 默认安装

> 默认端口2181

```yaml
---

- hosts: 192.168.77.129
  roles:
   - openjdk
   - zookeeper
```

### 单机伪集群安装

```yaml
---

- hosts: 192.168.77.129
  vars:
    - zookeeper_jmx_enabled: true
    - openjdk_packages: java-1.8.0-openjdk
    - zookeeper_config_extra: |
        audit.enable=true
    - zookeeper_hosts:
        - {'host': 192.168.77.129, 'id': 1, 'port': 2181, 'leader_port': '2888:3888'}
        - {'host': 192.168.77.129, 'id': 2, 'port': 2182, 'leader_port': '2889:3889'}
        - {'host': 192.168.77.129, 'id': 3, 'port': 2183, 'leader_port': '2890:3890'}
  roles:
   - openjdk
   - { role: zookeeper, zookeeper_client_port: 2181 }
   - { role: zookeeper, zookeeper_client_port: 2182 }
   - { role: zookeeper, zookeeper_client_port: 2183 }
```

### 分布式集群安装
    
默认参数

> zookeeper_hosts 为zookeeper集群主机的列表
```yaml
---

- hosts: 192.168.77.129 192.168.77.130 192.168.77.131
  vars:
    - zookeeper_hosts: "{{ ansible_play_hosts_all }}"
  roles:
   - openjdk
   - zookeeper
```

指定id
```yaml
---

- hosts: 192.168.77.129 192.168.77.130 192.168.77.131
  vars:
   - zookeeper_hosts:
      - {'host': 192.168.77.129, 'id': 1}
      - {'host': 192.168.77.130, 'id': 2}
      - {'host': 192.168.77.131, 'id': 3}
  roles:
   - openjdk
   - zookeeper
```

端口自定义
```yaml
---

- hosts: 192.168.77.129 192.168.77.130 192.168.77.131
  vars:
   - zookeeper_jmx_enabled: true
   - zookeeper_jmx_port: 10990
   - zookeeper_client_port: 2182
   - zookeeper_hosts:
      - {'host': 192.168.77.129, 'id': 1, 'port': 2182, 'leader_port': '2889:3889'}
      - {'host': 192.168.77.130, 'id': 2, 'port': 2182, 'leader_port': '2889:3889'}
      - {'host': 192.168.77.131, 'id': 3, 'port': 2182, 'leader_port': '2889:3889'}

  roles:
   - openjdk
   - zookeeper
```

## 使用

非systemd
```bash
/etc/init.d/zookeeper
Usage: /etc/init.d/zookeeper {start|stop|status|sstatus|restart|condrestart}

启动命令：/etc/init.d/zookeeper start 
关闭命令：/etc/init.d/zookeeper stop 
查看状态命令：/etc/init.d/zookeeper status 
客户端命令：zkCli.sh --config /data/zookeeper -server localhost:2181
```

systemd
```bash
启动命令：systemctl start zookeeper
关闭命令：systemctl stop zookeeper
查看状态命令：zkServer.sh --config /data/zookeeper status  
客户端命令：zkCli.sh --config /data/zookeeper -server localhost:2181
```