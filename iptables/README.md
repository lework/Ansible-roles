# Ansible Role: iptables

管理CentOS的iptables。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
	iptables_allowed_tcp_ports: ''
	iptables_allowed_udp_ports: ''
	iptables_deny_tcp_ports: ''
	iptables_deny_udp_ports: ''
	iptables_forwarded_tcp_ports: ''
	iptables_forwarded_udp_ports: ''
	iptables_additional_rules: ''
	action: 'insert'
	state: 'present'
	
## 依赖

没有

## github地址

https://github.com/kuailemy123/Ansible-roles/tree/master/iptables

## Example Playbook

    - hosts: server
      roles:
        - { role: iptables, iptables_allowed_tcp_ports: [ "22", "80"]}
		
	- hosts: server
      roles:
        - { role: iptables, iptables_allowed_tcp_ports: [ "22", "80"], state: 'absent'}

    - hosts: server
      roles:
	    - { role: iptables, iptables_forwarded_tcp_ports: - { role: iptables, iptables_forwarded_tcp_ports: [{ src: "80", dest: "8080" }, { src: "11", dest: "1111" }]}
		
	- hosts: server
      roles:
        - { role: iptables, iptables_additional_rules: "iptables -A INPUT -j DROP", action: "append"}	
