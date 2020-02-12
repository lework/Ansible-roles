# Ansible Role: redis5

安装 redis

## 介绍
Redis是一个使用ANSI C编写的开源、支持网络、基于内存、可选持久性的键值对存储数据库。从2015年6月开始，Redis的开发由Redis Labs赞助，而2013年5月至2015年6月期间，其开发由Pivotal赞助。在2013年5月之前，其开发由VMware赞助。

- 官方网站：https://redis.io/
- 官方文档地址：https://redis.io/documentation
- Github: https://github.com/antirez/redis-io

## 要求

此角色在Debian和RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: 2.9.1
    os: Centos 7.4 X64
    python: 2.7.5

ansible管理主机

    os: Centos 7, Debian 9

## 角色变量

```yaml
software_files_path: "/opt/software"
software_install_path: "/usr/local"

redis_version: "5.0.7"

redis_file: "redis-{{ redis_version }}.tar.gz"
redis_file_path: "{{ software_files_path }}/{{ redis_file }}"
redis_file_url: " http://download.redis.io/releases/{{ redis_file }}"

redis_user: redis
redis_group: redis
redis_port: 6379
redis_daemon: "redis{{ redis_port | default('') }}"


redis_data_path: "/data/redis"
redis_dir_path: "{{ redis_data_path }}/{{redis_port | default('6379')}}"
redis_dbdir: "{{ redis_dir_path }}/data"
redis_logdir: "{{ redis_dir_path }}/log"
redis_confdir: "{{ redis_dir_path }}/conf"

redis_log_file: "{{ redis_logdir }}/redis.log"
redis_conf_file: "{{ redis_confdir }}/redis.conf"


# redis配置
redis_bind_interface: 0.0.0.0
redis_timeout: 0
redis_loglevel: notice
redis_databases: 16
redis_maxmemory: 1024MB
redis_maxmemory_policy: volatile-ttl
redis_maxclients: 6000
redis_requirepass: ''
redis_appendonly: 'yes'
redis_save:
  - ""
#  - 900 1
#  - 300 10
#  - 60 10000

redis_rdbcompression: "yes"
redis_dbfilename: dump.rdb

# 从服务器配置
redis_slave: false
redis_master_host: ''
redis_master_port: ''


# 集群配置
redis_cluster: false
redis_masterauth: ''
redis_cluster_replicas: ''
# redis_cluster_replicas: '127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7010 127.0.0.1:7011 127.0.0.1:7012 --cluster-replicas 1 -a 123456'
# 上面有6个节点,程序会按照一定规则生成 3个master(主)3个slave(从)


# 哨兵配置
redis_sentinel: false
redis_sentinel_daemon: "redis-sentinel{{ redis_port | default('') }}"
redis_sentinel_log_file: "{{ redis_logdir }}/sentinel.log"
redis_sentinel_conf_file: "{{ redis_confdir }}/sentinel.conf"
redis_sentinel_monitors: 
  - name: mymaster
    ip: 127.0.0.1
    port: 6379
    quorum: 2
    masterauth: 123456

redis_rename_prefix: LE
redis_rename_commands:
  - FLUSHDB
  - FLUSHALL
  - KEYS
  - SAVE
  - RENAME
#  - PEXPIRE
#  - DEL
#  - CONFIG
#  - SHUTDOWN
#  - BGREWRITEAOF
#  - BGSAVE
#  - SPOP
#  - SREM
#  - DEBUG
# 前缀加个LE，重命名后变成LEFLUSHDB

redis_disabled_commands: []
#  - FLUSHDB
#  - FLUSHALL
#  - KEYS
```

## 依赖

无

## github地址

https://github.com/lework/Ansible-roles/tree/master/redis5

## Example Playbook
```yaml
# 默认安装
- hosts: 192.168.77.140
  roles:
   - redis5

# 定义端口和密码
- hosts: 192.168.77.140
  vars:
   - redis_port: 7000
   - redis_requirepass: 123456
  roles:
   - redis5
   
# 复制组
- hosts: 192.168.77.140
  vars:
    - redis_master_host: '127.0.0.1'
    - redis_master_port: '6380'
    - redis_requirepass: '123456'
    - redis_masterauth: '123456'
  roles:
   - { role: redis5,redis_port: 6380 }
   - { role: redis5,redis_port: 6381, redis_slave: true }
   - { role: redis5,redis_port: 6382, redis_slave: true }
   
# 哨兵模式
- hosts: 192.168.77.140
  vars:
    - redis_master_host: '192.168.77.140'
    - redis_master_port: '6380'
    - redis_requirepass: '123456'
    - redis_masterauth: '123456'
    - redis_sentinel_monitors:
      - name: mymaster
        ip: 192.168.77.140
        port: 6380
        quorum: 2
        masterauth: '123456'
  roles:
   - { role: redis5, redis_port: 6380 }
   - { role: redis5, redis_port: 6381, redis_slave: true }
   - { role: redis5, redis_port: 6382, redis_slave: true }
   - { role: redis5, redis_port: 16380, redis_sentinel: true }
   - { role: redis5, redis_port: 16381, redis_sentinel: true }
   - { role: redis5, redis_port: 16382, redis_sentinel: true }
  
# 集群模式
- hosts: 192.168.77.140
  vars:
    - redis_cluster: true 
    - redis_requirepass: '123456'
    - redis_masterauth: '123456'
  roles:
   - { role: redis5, redis_port: 7000 }
   - { role: redis5, redis_port: 7001 }
   - { role: redis5, redis_port: 7002 }
   - { role: redis5, redis_port: 7010 }
   - { role: redis5, redis_port: 7011 }
   - { role: redis5, redis_port: 7012, redis_cluster_replicas: '192.168.77.140:7000 192.168.77.140:7001 192.168.77.140:7002 192.168.77.140:7010 192.168.77.140:7011 192.168.77.140:7012 --cluster-replicas 1 -a 123456 --cluster-yes' }
```

## 使用

```
# systemd
systemctl status redis6380
systemctl start redis6380
systemctl stop redis6380
```