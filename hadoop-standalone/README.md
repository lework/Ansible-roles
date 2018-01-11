# Ansible Role: hadoop-standalone

以standalone方式安装hadoop

## 介绍
Hadoop是一个由Apache基金会所开发的分布式系统基础架构。
用户可以在不了解分布式底层细节的情况下，开发分布式程序。充分利用集群的威力进行高速运算和存储。

官方地址：http://hadoop.apache.org/
官方文档地址：http://hadoop.apache.org/docs/r2.7.3

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    hadoop_standalone_version: "2.7.3"

    hadoop_standalone_file: "hadoop-{{ hadoop_standalone_version }}.tar.gz"
    hadoop_standalone_file_path: "{{ software_files_path }}/{{ hadoop_standalone_file }}"
    hadoop_standalone_file_url: "https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-{{ hadoop_standalone_version }}/{{ hadoop_standalone_file }}"

    hadoop_standalone_user: "hadoop"

    hadoop_standalone_home: "{{ software_install_path }}/hadoop-{{ hadoop_standalone_version }}"

## 依赖

java

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/hadoop-standalone

## Example Playbook

    - hosts: node1
      roles:
        - { role: hadoop-standalone }