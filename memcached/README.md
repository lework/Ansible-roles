# Ansible Role: Memcached

安装Memcached

## 介绍
Memcached 是一个高性能的分布式内存对象缓存系统，用于动态Web应用以减轻数据库负载。它通过在内存中缓存数据和对象来减少读取数据库的次数，从而提高动态、数据库驱动网站的速度。Memcached基于一个存储键/值对的hashmap。其守护进程（daemon ）是用C写的，但是客户端可以用任何语言来编写，并通过memcached协议与守护进程通信。

官方网站：http://memcached.org/
github地址： https://github.com/memcached/memcached

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    memcached_version: "1.4.33"

    memcached_file: "memcached-{{ memcached_version }}.tar.gz"
    memcached_file_path: "{{ software_files_path }}/{{ memcached_file }}"
    memcached_file_url: "http://memcached.org/files/memcached-{{ memcached_version }}.tar.gz"

    memcached_listen_ip: 0.0.0.0
    memcached_daemon: "memcached{{ memcached_port | default('') }}"

    memcached_cachesize: 64
    memcached_maxconn: 1024

    memcached_log_file: /var/log/memcached{{ memcached_port | default('') }}.log
    memcached_log_verbosity: "-vv"
    memcached_options: "-l {{ memcached_listen_ip }} {{ memcached_log_verbosity }} 2>> {{ memcached_log_file }}"
    

## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/memcached

## Example Playbook

    安装memcached，默认端口11211
    - hosts: node1
      roles:
        - { role: memcached }

    指定端口
    - hosts: node1
      roles:
        - { role: memcached, memcached_port: 11222 }
