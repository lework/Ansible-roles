# Ansible Role: consul

安装consul

## 介绍
consul是HashiCorp公司推出的一款开源工具，用于实现分布式系统的服务发现与配置。与其他类似产品相比，提供更“一站式”的解决方案。consul内置有KV存储，服务注册/发现，健康检查，HTTP+DNS API，Web UI等多种功能。

官方地址： https://www.consul.io/
github: https://github.com/hashicorp/consul
官方文档地址：https://www.consul.io/docs

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	hadoop_version: "2.7.3"

	hadoop_file: "hadoop-{{ hadoop_version }}.tar.gz"
	hadoop_file_path: "{{ software_files_path }}/{{ hadoop_file }}"
	hadoop_file_url: "https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-{{ hadoop_version }}/{{ hadoop_file }}"

	hadoop_user: "hadoop"

	hadoop_home: "{{ software_install_path }}/hadoop-{{ hadoop_version }}"

## 依赖

supervisor

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/consul

## Example Playbook

	安装consul：
	- hosts: 192.168.77.129
	  vars:
		supervisor_name: consul
		supervisor_stopsignal: INT
		supervisor_program: 
		  - { name: 'consul', command: 'consul agent -config-file /consul_data/conf/basic_config.json', user: 'consul' }
	  roles:
	   - { role: consul }
	   - { role: python2.7 }
	   - { role: supervisor }


	分布式安装：
	端口默认
	- hosts: 192.168.77.129
	  roles:
		- { role: consul, consul_bootstrap: true }

	- hosts: 192.168.77.130 192.168.77.131
	  roles:
	   - { role: consul, consul_bootstrap_expect: false, consul_start_join: ["192.168.77.129"]}

	- hosts: 192.168.77.132
	  roles:
	  - { role: consul, consul_server: false, consul_start_join: ["192.168.77.129"]}

	- hosts: all
	  vars:
		supervisor_name: consul
		supervisor_stopsignal: INT
		supervisor_program: 
		  - { name: 'consul', command: 'consul agent -config-file /consul_data/conf/basic_config.json', user: 'consul' }
	  roles:
	   - { role: python2.7 }
	   - { role: supervisor }