# Ansible Role: Mysql

安装mysql

## 介绍
MySQL是一个关系型数据库管理系统，由瑞典MySQL AB 公司开发，目前属于 Oracle 旗下产品。MySQL 是最流行的关系型数据库管理系统之一，在 WEB 应用方面，MySQL是最好的 RDBMS (Relational Database Management System，关系数据库管理系统) 应用软件。


官方地址： https://www.mysql.com/
官方文档地址：https://dev.mysql.com/doc/refman/5.6/en/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

os `Centos 7.2 X64`

python `2.7.5`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    mysql_version: "5.6.39"

    mysql_file: "mysql-{{ mysql_version }}.tar.gz"
    mysql_file_path: "{{ software_files_path }}/{{ mysql_file }}"
    mysql_file_url: "https://cdn.mysql.com/Downloads/MySQL-5.6/mysql-{{ mysql_version }}.tar.gz"
    mysql_dirname: "mysql-{{ mysql_version }}"

    mysql_port: "3306"
    mysql_user: "root"
    mysql_password: "123456"
    mysql_datahome: "/mysql_data"
    mysql_basedir: "{{ software_install_path }}/mysql"
    mysql_portdir: "{{ mysql_datahome }}/{{ mysql_port }}"
    mysql_datadir: "{{ mysql_datahome }}/{{ mysql_port }}/data"
    mysql_cnf : "{{ mysql_datahome }}/{{ mysql_port }}/my.cnf"
    mysql_sock : "{{ mysql_datahome }}/{{ mysql_port }}/mysql.sock"
    mysql_startsh : "{{ mysql_datahome }}/{{ mysql_port }}/mysql{{ mysql_port }}.sh"

    mysql_install_from_source: false
    mysql_source_configure_command: >
      /usr/bin/cmake -DCMAKE_INSTALL_PREFIX={{ software_install_path }}/mysql-{{ mysql_version }}
      -DMYSQL_UNIX_ADDR={{ mysql_sock }}
      -DDEFAULT_CHARSET=utf8mb4
      -DDEFAULT_COLLATION=utf8mb4_unicode_ci
      -DWITH_EXTRA_CHARSETS:STRING=all
      -DWITH_MYISAM_STORAGE_ENGINE=1
      -DWITH_INNOBASE_STORAGE_ENGINE=1
      -DWITH_MEMORY_STORAGE_ENGINE=1
      -DWITH_PARTITION_STORAGE_ENGINE=1
      -DWITH_READLINE=1
      -DENABLED_LOCAL_INFILE=1
      -DMYSQL_DATADIR={{ mysql_datadir }}
      -DMYSQL_USER=mysql
      -DMYSQL_TCP_PORT={{ mysql_port }}
      -DWITH_SSL=system
            
    mysql_replication_user: {name: 'rep', password: '123456'}
    mysql_replication_master: ''
    mysql_replication_master_port: "3306"
    mysql_replication_role: ''
    mysql_auto_increment_offset: ''

    mysql_binlog_format: "STATEMENT"
    

## 依赖

gcc cmake

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/mysql

## Example Playbook

    使用bin文件安装(已编译好的mysql，文件/opt/software/mysql-5.6.10-bin.tar.gz)：
    - hosts: node1
      roles:
       - { role: mysql }

    源码安装：
    - hosts: node1
      roles:
       - { role: mysql , mysql_install_from_source: true }

    主从安装：
    - hosts: node1
      roles:
       - { role: mysql, mysql_replication_role: 'master'}
       - { role: mysql, mysql_port: 3307, mysql_replication_role: 'slave', mysql_replication_master: '192.168.77.129'}
    
    互为主备安装：
    - hosts: node1
      roles:
       - { role: mysql, mysql_port: 3306, mysql_replication_role: 'master', auto_increment_offset: 1}
       - { role: mysql, mysql_port: 3307, mysql_replication_role: 'slave', mysql_replication_master: '192.168.77.129', auto_increment_offset: 2}
       - { role: mysql, mysql_port: 3307, mysql_replication_role: 'master' }
       - { role: mysql, mysql_port: 3306, mysql_replication_role: 'slave', mysql_replication_master: '192.168.77.129', mysql_replication_master_port: 3307}


## 使用

启动命令：/mysql_data/3306/mysql3306.sh start
关闭命令：/mysql_data/3306/mysql3306.sh stop