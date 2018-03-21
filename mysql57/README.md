# Ansible Role: Mysql 5.7

安装mysql 5.7

## 介绍
MySQL是一个关系型数据库管理系统，由瑞典MySQL AB 公司开发，目前属于 Oracle 旗下产品。MySQL 是最流行的关系型数据库管理系统之一，在 WEB 应用方面，MySQL是最好的 RDBMS (Relational Database Management System，关系数据库管理系统) 应用软件。


官方地址： https://www.mysql.com/

官方文档地址：https://dev.mysql.com/doc/refman/5.7/en/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

os `Centos 7.2 X64`

python `2.7.5`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    mysql57_version: "5.7.20"

    mysql57_file: "mysql-boost-{{ mysql57_version }}.tar.gz"
    mysql57_bin_file: "mysql-boost-{{ mysql57_version }}-bin.tar.gz"
    mysql57_file_path: "{{ software_files_path }}/{{ mysql57_file }}"
    mysql57_file_url: "https://cdn.mysql.com/Downloads/MySQL-5.7/{{ mysql57_file }}"
    mysql57_dirname: "mysql-{{ mysql57_version }}"

    mysql57_port: "3306"
    mysql57_user: "root"
    mysql57_password: "123456"
    mysql57_datahome: "/mysql_data"
    mysql57_basedir: "{{ software_install_path }}/mysql-{{ mysql57_version }}"
    mysql57_portdir: "{{ mysql57_datahome }}/{{ mysql57_port }}"
    mysql57_datadir: "{{ mysql57_portdir }}/data"
    mysql57_cnf : "{{ mysql57_portdir }}/my.cnf"
    mysql57_sock : "{{ mysql57_portdir }}/mysql.sock"
    mysql57_servicename : "mysql{{ mysql57_port }}"

    mysql57_install_from_source: false
    mysql57_source_configure_command: >
      /usr/bin/cmake -DCMAKE_INSTALL_PREFIX={{ mysql57_basedir }}
      -DMYSQL_DATADIR={{ mysql57_datadir }}
      -DSYSCONFDIR={{ mysql57_portdir }}
      -DMYSQL_USER=mysql
      -DMYSQL_TCP_PORT={{ mysql57_port }}
      -DWITH_MYISAM_STORAGE_ENGINE=1
      -DWITH_INNOBASE_STORAGE_ENGINE=1
      -DWITH_ARCHIVE_STORAGE_ENGINE=1
      -DWITH_MEMORY_STORAGE_ENGINE=1
      -DWITH_PARTITION_STORAGE_ENGINE=1
      -DWITH_INNODB_MEMCACHED=1
      -DMYSQL_UNIX_ADDR={{ mysql57_sock }}
      -DWITH_SSL=system
      -DWITH_ZLIB=system
      -DENABLED_LOCAL_INFILE=1
      -DENABLE_DOWNLOADS=1
      -DWITH_READLINE=1
      -DENABLED_LOCAL_INFILE=1
      -DEXTRA_CHARSETS=all
      -DDEFAULT_CHARSET=utf8mb4
      -DDEFAULT_COLLATION=utf8mb4_general_ci
      -DWITH_BOOST=boost

    mysql57_innodb_buffer_pool_size: "512M"
    mysql57_replication_user: {name: 'rep', password: '123456'}
    mysql57_replication_master: "127.0.0.1"
    mysql57_replication_master_port: "3306"
    mysql57_replication_role: ""
    mysql57_auto_increment_offset: "1"
    mysql57_auto_increment_increment: "1"

    mysql57_replication_mode: "gtid"
    mysql57_binlog_format: "ROW"

    mysql57_replication_channel: {}

    mysql57_replication_ga: false
    mysql57_replication_ga_first: false
    mysql57_replication_ga_single: false
    mysql57_group_replication_start_on_boot: "off"
    mysql57_group_replication_group_name: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    mysql57_group_recation_local_address: "127.0.0.1:24901"
    mysql57_group_replication_group_seeds: "127.0.0.1:24901,127.0.0.1:24902,127.0.0.1:24903"
    

## 依赖

gcc cmake boost

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/mysql57

## Example Playbook

    默认安装, 使用bin文件(已编译好的mysql),文件/opt/software/mysql-boost-5.7.20-bin.tar.gz)：
    - hosts: node2
      roles:
      - mysql57

    源码编译安装
    - hosts: node2
      roles:
      - { role: mysql57, mysql57_install_from_source: true }
      
    指定端口
    - hosts: node2
      roles:
      - { role: mysql57, mysql57_port: "3307" }

    默认使用gitd方式配置主从
    - hosts: node2
      roles:
      - { role: mysql57, mysql57_replication_role: 'master'}
      - { role: mysql57, mysql57_port: 3307, mysql57_replication_role: 'slave', mysql57_replication_master: '192.168.77.130'}

    采用file方式配置主从
    - hosts: node2
      vars:
      - mysql57_replication_mode: 'file' # 指定binlog方式为file pos
      roles:
      - { role: mysql57, mysql57_replication_role: 'master'}
      - { role: mysql57, mysql57_port: 3307, mysql57_replication_role: 'slave', mysql57_replication_master: '192.168.77.130'}

    主主配置
    - hosts: node2
      roles:
      - role: 'mysql57'
        mysql57_port: '3306'
        mysql57_replication_role: 'master'
        mysql57_replication_user: {name: 'rep_3306', password: '123456'}

      - role: 'mysql57'
        mysql57_port: '3307'
        mysql57_replication_role: 'master'
        mysql57_replication_user: {name: 'rep_3307', password: '123456'}
        
      - role: 'mysql57'
        mysql57_port: '3306'
        mysql57_auto_increment_offset: '1'
        mysql57_auto_increment_increment: '2'
        mysql57_replication_role: 'slave' # 指定为slave角色
        mysql57_replication_master: '192.168.77.130'
        mysql57_replication_master_port: '3307'
        mysql57_replication_user: {name: 'rep_3307', password: '123456'}

      - role: 'mysql57'
        mysql57_port: '3307'
        mysql57_auto_increment_offset: '2'
        mysql57_auto_increment_increment: '2'
        mysql57_replication_role: 'slave'
        mysql57_replication_master: '192.168.77.130'
        mysql57_replication_master_port: '3306'
        mysql57_replication_user: {name: 'rep_3306', password: '123456'}

    多源复制
    - hosts: node2
      roles:
      - role: 'mysql57'
        mysql57_port: '3306' 
        mysql57_binlog_format: 'mixed'
        mysql57_auto_increment_offset: '1'
        mysql57_auto_increment_increment: '2'
        mysql57_replication_role: 'master'
        mysql57_replication_user: {name: 'rep_3306', password: '123456'}

      - role: 'mysql57'
        mysql57_port: '3307'
        mysql57_binlog_format: 'mixed'
        mysql57_auto_increment_offset: '2'
        mysql57_auto_increment_increment: '2'
        mysql57_replication_role: 'master'
        mysql57_replication_user: {name: 'rep_3307', password: '123456'}
        
      - role: 'mysql57'
        mysql57_port: '3308'
        mysql57_replication_role: 'slave'
        mysql57_replication_channel:  # 指定通道链接
        - master_host: "192.168.77.130"
          master_port: "3306"
          master_user: "rep_3306"
          master_password: "123456"
        - master_host: "192.168.77.130"
          master_port: "3307"
          master_user: "rep_3307"
          master_password: "123456" 
        
    组复制
    - hosts: node2
      vars:
      - mysql57_replication_ga: true  # 开启组复制
      - mysql57_replication_role: 'master' # 指定为master角色
      - mysql57_group_replication_group_name: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"  # 指定组名
      - mysql57_group_replication_group_seeds: "192.168.77.130:24901,192.168.77.130:24902,192.168.77.130:24903" # 指定组内的成员
      - mysql57_replication_user: {name: 'rep', password: '123456'} # 指定用于复制的账号
      - ipnames:  # 指定ip和主机名的对应关系，这里使用单机多实例。
         '192.168.77.130': 'node2'

      roles:
      - role: 'mysql57'
        mysql57_port: '3306'  
        mysql57_group_recation_local_address: "192.168.77.130:24901"  # 指定组监听地址
        mysql57_replication_ga_first: true # 指定组内第一成员

      - role: 'mysql57'
        mysql57_port: '3307'
        mysql57_group_recation_local_address: "192.168.77.130:24902"
        
      - role: 'mysql57'
        mysql57_port: '3308'
        mysql57_group_recation_local_address: "192.168.77.130:24903"

       
## 使用

启动命令：`systemctl start mysql3306`

关闭命令：`systemctl stop mysql3306`

重启命令：`systemctl restart mysql3306`