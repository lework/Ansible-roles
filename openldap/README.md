# Ansible Role: openldap

安装openldap服务

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.8.1`
os `Centos 7.4 X64`

## 角色变量
	openldap_packages:
	  - openldap
	  - compat-openldap
	  - openldap-clients
	  - openldap-servers
	  - openldap-servers-sql
	  - openldap-devel
	  - migrationtools
	  - rsyslog

	openldap_dc: "dc=lework,dc=com"
	openldap_passwd: 123456
	openldap_log: /var/log/slapd.log

## 依赖

没有

## github地址
https://github.com/lework/Ansible-roles/tree/master/openldap

## Example Playbook

	# 默认安装
	---
	- hosts: 192.168.77.131
	  roles:
	   - openldap
	   

	# 指定dc和密码
	---
	- hosts: 192.168.77.131
	  vars:
	   - openldap_dc: dc=lework,dc=local
	   - openldap_passwd: abcdefg
	  roles:
	   - openldap