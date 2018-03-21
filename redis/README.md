# Ansible Role: Redis

安装redis

## 介绍
redis（Remote Dictionary Server）是一个key-value存储系统。和Memcached类似，它支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。这些数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。在此基础上，redis支持各种不同方式的排序。与memcached一样，为了保证效率，数据都是缓存在内存中。区别的是redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。

官方地址： https://redis.io/
官方文档地址：https://redis.io/documentation

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

os `Centos 7.2 X64`

python `2.7.5`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    redis_version: "3.2.11"

    redis_file: "redis-{{ redis_version }}.tar.gz"
    redis_file_path: "{{ software_files_path }}/{{ redis_file }}"
    redis_file_url: "http://download.redis.io/releases/redis-{{ redis_version }}.tar.gz"

    redis_data_path: "/redis_data"
    # redis_port: 6379
    redis_daemon: "redis{{ redis_port | default('') }}"
    redis_dir_path: "{{ redis_data_path }}/{{redis_port | default('6379')}}"

    redis_timeout: 0
    redis_user: redis

    redis_loglevel: "notice"
    redis_logfile: "{{ redis_dir_path }}/redis-server.log"
    redis_pidfile: "{{ redis_dir_path }}/redis.pid"

    redis_databases: 16

    redis_rdbcompression: "yes"
    redis_dbfilename: dump.rdb
    redis_dbdir: "{{ redis_dir_path }}/data"

    redis_maxmemory: "1000mb"

    redis_requirepass: ''
    redis_slave: false
    redis_cluster: false
    redis_cluster_replicas: ''
    # redis_cluster_replicas: '1 127.0.0.1:6481 127.0.0.1:6482 127.0.0.1:6483 127.0.0.1:6484 127.0.0.1:6485 127.0.0.1:6486'
    # 1 表示 自动为每一个master节点分配一个slave节点, 上面有6个节点,程序会按照一定规则生成 3个master(主)3个slave(从)
    redis_masterauth: ''
    redis_master_host: ''
    redis_master_port: ''

    redis_sentinel_port: ''
    redis_sentinel_quorum: '2'
    redis_sentinel_daemon: "redis-sentinel{{ redis_sentinel_port | default('') }}"
    

## 依赖

java ruby

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/redis

## Example Playbook

    单实例安装
    - hosts: node1
      roles:
        - { role: redis }
        
    主从配置
    - hosts: node1
      vars:
       - redis_master_host: '127.0.0.1'
       - redis_master_port: '6380'
      roles:
        - { role: redis, redis_port: 6380}
        - { role: redis, redis_port: 6381, redis_slave: true}
        - { role: redis, redis_port: 6382, redis_slave: true}
        
    哨兵模式
    - hosts: node1
      vars:
       - redis_master_host: '127.0.0.1'
       - redis_master_port: '6383'
      roles:
       - { role: redis, redis_port: 6383, redis_sentinel_port: 26383}
       - { role: redis, redis_port: 6384, redis_sentinel_port: 26384, redis_slave: true}
       - { role: redis, redis_port: 6385, redis_sentinel_port: 26385, redis_slave: true}


     伪集群模式
     - hosts: node1
       vars:
        - redis_cluster: true
        - redis_requirepass: '123456'
       roles:
        - { role: redis, redis_port: 6481}
        - { role: redis, redis_port: 6482}
        - { role: redis, redis_port: 6483}
        - { role: redis, redis_port: 6484}
        - { role: redis, redis_port: 6485}
        - { role: redis, redis_port: 6486, redis_cluster_replicas: '1 127.0.0.1:6481 127.0.0.1:6482 127.0.0.1:6483 127.0.0.1:6484 127.0.0.1:6485 127.0.0.1:6486'}

    集群分布式模式
     - hosts: node1
       vars:
        - redis_cluster: true
        - redis_requirepass: '123456'
       roles:
        - { role: redis, redis_port: 7000}
        - { role: redis, redis_port: 7003}

     - hosts: node2
       vars:
        - redis_cluster: true
        - redis_requirepass: '123456'
       roles:
        - { role: redis, redis_port: 7001}
        - { role: redis, redis_port: 7004}

     - hosts: node3
       vars:
        - redis_cluster: true
        - redis_requirepass: '123456'
       roles:
        - { role: redis, redis_port: 7002}
        - { role: redis, redis_port: 7005, redis_cluster_replicas: '1 172.19.204.246:7000 172.19.204.245:7001 172.19.204.244:7002 172.19.204.246:7003 172.19.204.245:7004 172.19.204.244:7005'}
