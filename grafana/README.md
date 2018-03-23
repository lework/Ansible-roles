# Ansible Role: grafana

安装grafana

## 介绍
Grafana 是 Graphite 和 InfluxDB 仪表盘和图形编辑器。Grafana 是开源的，功能齐全的度量仪表盘和图形编辑器，支持 Graphite，InfluxDB 和 OpenTSDB。

官方地址：https://grafana.com/
github: https://github.com/grafana/grafana
官方文档地址：http://docs.grafana.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
	software_files_path: "/opt/software"

	grafana_version: "4.4.1"
	grafana_package_url: "https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-{{ grafana_version }}-1.x86_64.rpm"

	grafana_plugins: []

	grafana_http_port: 3000
	grafana_admin_user: "admin"
	grafana_admin_password: "admin"

## 依赖

None

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/grafana

## Example Playbook
     - hosts: node1
       roles:
        - grafana
		
     - hosts: node1
       vars:
        - grafana_plugins:
           - alexanderzobnin-zabbix-app
        - grafana_admin_password: '123456'
       roles:
        - { role: grafana }
        - { role: iptables, iptables_allowed_tcp_ports: [ "3000"]}

## 使用

```
~]# /etc/init.d/grafana-server 
Usage: /etc/init.d/grafana-server {start|stop|restart|force-reload|status}

```
