# Ansible Role: zabbix-server

安装zabbix server

## 介绍
zabbix（音同 z?bix）是一个基于WEB界面的提供分布式系统监视以及网络监视功能的企业级的开源解决方案。
zabbix server可以通过SNMP，zabbix agent，ping，端口监视等方法提供对远程服务器/网络状态的监视，数据收集等功能，它可以运行在Linux，Solaris，HP-UX，AIX，Free BSD，Open BSD，OS X等平台上。

官方地址： https://www.zabbix.com
官方文档地址：https://www.zabbix.com/documentation/3.2/manual

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.1`

os `Centos 7.2.1511 X64`

python `2.7.5`

## 角色变量

    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    zabbix_server_version: "3.4.8"

    zabbix_server_file: "zabbix-{{ zabbix_server_version }}.tar.gz"
    zabbix_server_file_path: "{{ software_files_path }}/{{ zabbix_server_file }}"
    zabbix_server_file_url: "https://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/{{ zabbix_server_version }}/{{ zabbix_server_file }}"

    zabbix_server_packages:
      - "zabbix-server-mysql-{{ zabbix_server_version }}"
      - "zabbix-web-mysql-{{ zabbix_server_version }}"
      - "zabbix-agent-{{ zabbix_server_version }}"

    zabbix_server_user: zabbix
    zabbix_server_group: zabbix
    zabbix_server_hostanme: "Zabbix server"

    zabbix_server_install_from_source: false

    zabbix_server_source_dir: "/tmp/{{ zabbix_server_file | replace('.tar.gz','') }}"
    zabbix_server_source_configure_command: >
      ./configure
      --prefix={{ software_install_path }}/zabbix-{{ zabbix_server_version }}
      --enable-server
      --enable-agent
      --with-mysql
      --enable-ipv6
      --with-net-snmp
      --with-libcurl
      --with-libxml2

    zabbix_server_conf_path: "/etc/zabbix" 
    zabbix_server_logs_path: "/var/log/zabbix"
    zabbix_server_webroot: "/var/www/html/zabbix"
    zabbix_server_webserver: "httpd"
    zabbix_server_webserver_user: "apache"

    zabbix_server_db: zabbix
    zabbix_server_db_host: "127.0.0.1"
    zabbix_server_db_port: "3306"
    zabbix_server_db_user: "zabbix"
    zabbix_server_db_password: "zabbix"

## 依赖

Mysql, Httpd, PHP

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/zabbix-server

## Example Playbook

    源码安装
    ---
    # 配置web服务器和mysql服务器
    - hosts: node4
      vars:
        - zabbix_server_db: zabbix
        - zabbix_server_db_user: zabbix
        - zabbix_server_db_password: zabbix
        - zabbix_server_db_host: 127.0.0.1
      roles:
        - { role: mysql57 , mysql57_password: "123456" }
        - { role: php, php_httpd_enable: true, php_install_from_source: true }

      tasks:
        - name: configure_db | Create zabbix database.
          shell: source /etc/profile; mysql -uroot -p123456 -h192.168.77.133 -P3306 -e "{{ item }}"
          with_items:
            - "create database {{ zabbix_server_db }} character set utf8 collate utf8_bin;"
            - "grant all privileges on {{  zabbix_server_db }}.* to '{{ zabbix_server_db_user }}'@'{{ zabbix_server_db_host }}' identified by '{{ zabbix_server_db_password }}';"
    # 配置zabbix-server
    - hosts: node4
      vars:
        - zabbix_server_db: zabbix
        - zabbix_server_db_user: zabbix
        - zabbix_server_db_password: zabbix
        - zabbix_server_db_host: 127.0.0.1
        - zabbix_server_install_from_source: true

      roles:
        - zabbix-server
    
    rpm方式安装
    ---
    # 配置web服务器和mysql服务器
    - hosts: node4
      vars:
        - zabbix_server_db: zabbix
        - zabbix_server_db_user: zabbix
        - zabbix_server_db_password: zabbix
        - zabbix_server_db_host: 127.0.0.1
      roles:
        - { role: mysql57 , mysql57_password: "123456" }

      tasks:
        - name: configure_db | Create zabbix database.
          shell: source /etc/profile; mysql -uroot -p123456 -h192.168.77.133 -P3306 -e "{{ item }}"
          with_items:
            - "create database {{ zabbix_server_db }} character set utf8 collate utf8_bin;"
            - "grant all privileges on {{  zabbix_server_db }}.* to '{{ zabbix_server_db_user }}'@'{{ zabbix_server_db_host }}' identified by '{{ zabbix_server_db_password }}';"
    # 配置zabbix-server
    - hosts: node4
      vars:
        - zabbix_server_db: zabbix
        - zabbix_server_db_user: zabbix
        - zabbix_server_db_password: zabbix
        - zabbix_server_db_host: 127.0.0.1

      roles:
        - zabbix-server
   
## 使用

```
~]# /etc/init.d/zabbix-server 
Usage: /etc/init.d/zabbix-server {start|stop|status|restart|try-restart|force-reload}

systemctl status zabbix-server
```
