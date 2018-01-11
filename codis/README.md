# Ansible Role: Codis

安装Codis集群

## 介绍
Codis 是一个分布式 Redis 解决方案, 对于上层的应用来说, 连接到 Codis Proxy 和连接原生的 Redis Server 没有显著区别 (不支持的命令列表), 上层应用可以像使用单机的 Redis 一样使用, Codis 底层会处理请求的转发, 不停机的数据迁移等工作, 所有后边的一切事情, 对于前面的客户端来说是透明的, 可以简单的认为后边连接的是一个内存无限大的 Redis 服务。

github地址：https://github.com/CodisLabs/codis
使用文档：https://github.com/CodisLabs/codis/blob/release3.2/doc/tutorial_zh.md

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	codis_version: "3.1.3"

	codis_file: "codis-{{ codis_version }}.tar.gz"
	codis_file_path: "{{ software_files_path }}/{{ codis_file }}"
	codis_file_url: "https://github.com/CodisLabs/codis/archive/{{ codis_version }}.tar.gz"

	codis_basedir: "{{ software_install_path }}/codis"
	codis_conf_path: "{{ codis_basedir }}/conf"
	codis_bin_path: "{{ codis_basedir }}/bin"

	codis_server: false
	codis_server_port: 6379
	codis_server_daemon: "codis-server{{ codis_server_port }}"
	codis_server_requirepass: 'rtest'
	codis_server_masterauth: 'rtest'

	codis_server_sentinel_port: ''
	codis_server_sentinel_quorum: 2
	codis_server_sentinel_daemon: "codis-server-sentinel{{ codis_server_sentinel_port }}"
	codis_server_sentinel_monitor_name: 'master1'
	codis_server_sentinel_addr: ''
	codis_server_master_host:  "{{ ansible_default_ipv4.address }}"
	codis_server_master_port: "6379"

	codis_data_path: "/codis_data"
	codis_gopath: "{{ codis_data_path }}/gopath" 
	codis_labs_path: "{{ codis_gopath }}/src/github.com/CodisLabs"
	codis_server_data_path: "{{ codis_data_path}}/codis-server_{{ codis_server_port }}"
	codis_server_logs_path: "{{ codis_data_path}}/logs/codis-server"
	codis_pid_path: "{{ codis_data_path }}/pid"

	codis_loglevel: "WARN"
	codis_bind_address: "0.0.0.0"
	codis_ncpu: 1

	codis_product_name: "codis-demo"
	codis_coordinator_name: "zookeeper"

	codis_admin_prot: 11080
	codis_admin_addr: "0.0.0.0:{{ codis_admin_prot }}"

	codis_fe: false
	codis_fe_port: 8080
	codis_fe_listen: "0.0.0.0:{{ codis_fe_port }}"
	codis_fe_logs_path: "{{ codis_data_path}}/logs/fe"

	codis_ha: false
	codis_ha_logs_path: "{{ codis_data_path}}/logs/ha"
	codis_admin: false

	codis_dashboard: false
	codis_dashboard_port: 18080
	codis_dashboard_addr: "0.0.0.0:{{ codis_codis_dashboard_port_prot }}"
	codis_dashboard_logs_path: "{{ codis_data_path}}/logs/dashboard"

	codis_proxy: false
	codis_proxy_port: 19000
	codis_proxy_addr: "0.0.0.0:{{ codis_proxy_port }}"
	codis_proxy_logs_path: "{{ codis_data_path}}/logs/proxy"

	install: true
	zookeeper_hosts: []
	codis_groups: []
	codis_group_master_server: []
	codis_group_slave_server: []
	codis_proxy_addrs: []
	
## 依赖

go
zookeeper

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/codis

## Example Playbook

	部署集群
	IP		主机名		部署程序
	192.168.77.129    node1	zookeeper codis-group codis-proxy sentinel codis-dashboard codis-fe codis-ha
	192.168.77.130    node2	zookeeper codis-group codis-proxy sentinel
	192.168.77.131    node3	zookeeper codis-group codis-proxy sentinel
	 
    - hosts: 192.168.77.129 192.168.77.130 192.168.77.131
      vars:
        - codis_version: "3.1.5"
        - zookeeper_hosts:
          - {'host': 192.168.77.129, 'id': 1}
          - {'host': 192.168.77.130, 'id': 2}
          - {'host': 192.168.77.131, 'id': 3}
      roles:
        - { role: zookeeper }
        - { role: codis, codis_server: true, codis_server_port: 6379, codis_server_sentinel_port: 26379}
        - { role: codis, install: false, codis_server: true, codis_server_port: 6380, codis_server_sentinel_port: 26380 }
        - { role: codis, install: false, codis_proxy: true }

    - hosts: 192.168.77.129
      vars:
        - zookeeper_hosts:
          - {'host': 192.168.77.129, 'id': 1}
          - {'host': 192.168.77.130, 'id': 2}
          - {'host': 192.168.77.131, 'id': 3}
        - codis_dashboard_addr: 192.168.77.129:18080
        - codis_groups: [1,2,3] 
        - codis_group_master_server:
          - {'gid': 1, 'addr': '192.168.77.129:6379'}
          - {'gid': 2, 'addr': '192.168.77.130:6379'}
          - {'gid': 3, 'addr': '192.168.77.131:6379'}
        - codis_group_slave_server:
          - {'gid': 1, 'addr': '192.168.77.129:6380'}
          - {'gid': 2, 'addr': '192.168.77.130:6380'}
          - {'gid': 3, 'addr': '192.168.77.131:6380'}
        - codis_proxy_addrs:
          - 192.168.77.129:11080
          - 192.168.77.130:11080
          - 192.168.77.131:11080
        - codis_server_sentinel_addr:
          - 192.168.77.129:26379
          - 192.168.77.129:26380
          - 192.168.77.130:26379
          - 192.168.77.130:26380
          - 192.168.77.131:26379
          - 192.168.77.131:26380
      roles:
        - { role: codis, install: false, codis_dashboard: true }
        - { role: codis, install: false, codis_fe: true }
        - { role: codis, install: false, codis_admin: true }
        - { role: codis, install: false, codis_ha: true }
	
	安装sentinel
    - hosts: 192.168.77.129
      vars:
        - codis_server_master_host: 192.168.77.129
        - codis_server_master_port: 6379
        - codis_server_sentinel_addr: 
          - 192.168.77.129：26381
      roles:
        - { role: codis, install: false, codis_server_sentinel_port: 26381}
        - { role: codis, install: false, codis_admin: true }
