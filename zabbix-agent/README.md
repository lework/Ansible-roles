# Ansible Role: zabbix-agent

安装zabbix客户端

## 介绍
zabbix（音同 z?bix）是一个基于WEB界面的提供分布式系统监视以及网络监视功能的企业级的开源解决方案。
zabbix agent需要安装在被监视的目标服务器上，它主要完成对硬件信息或与操作系统有关的内存，CPU等信息的收集。zabbix agent可以运行在Linux,Solaris,HP-UX,AIX,Free BSD,Open BSD, OS X, Tru64/OSF1, Windows NT4.0, Windows (2000/2003/XP/Vista)等系统之上。

官方地址： https://www.zabbix.com
官方文档地址：https://www.zabbix.com/documentation/3.2/manual

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.1`

os `Centos 7.2.1511 X64`

python `2.7.5`

supervisor `3.3.4`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    zabbix_agent_version: "3.4.8"

    zabbix_agent_file: "zabbix-{{ zabbix_agent_version }}.tar.gz"
    zabbix_agent_file_path: "{{ software_files_path }}/{{ zabbix_agent_file }}"
    zabbix_agent_file_url: "https://phoenixnap.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/{{ zabbix_agent_version }}/{{ zabbix_agent_file }}"

    zabbix_agent_packages:
      - "zabbix-agent-{{ zabbix_agent_version }}"

    zabbix_agent_user: zabbix
    zabbix_agent_group: zabbix

    zabbix_agent_install_from_source: false

    zabbix_agent_source_dir: "/tmp/{{ zabbix_agent_file | replace('.tar.gz','') }}"
    zabbix_agent_source_configure_command: >
      ./configure
      --prefix={{ software_install_path }}/zabbix-{{ zabbix_agent_version }}
      --enable-agent

    zabbix_agent_conf_path: "/etc/zabbix" 
    zabbix_agent_logs_path: "/var/log/zabbix"

    zabbix_agent_hostname: "{{ ansible_hostname | d() }}"
    zabbix_agent_server_host: "127.0.0.1"

## 依赖

zabbix server

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/zabbix-agent

## Example Playbook
    ---
    # 源码安装
    - hosts: node2
      roles:
       - { role: zabbix-agent, zabbix_agent_install_from_source: true, zabbix_agent_server_host: "192.168.77.130" }
       
    # rpm包安装
    - hosts: node3
      roles:
       - { role: zabbix-agent, zabbix_agent_server_host: "192.168.77.130" }


## 使用

```
~]# /etc/init.d/zabbix-agent 
Usage: /etc/init.d/zabbix-agent {start|stop|status|restart|help}

    start        - start zabbix_agentd
    stop        - stop zabbix_agentd
    status        - show current status of zabbix_agentd
    restart        - restart zabbix_agentd if running by sending a SIGHUP or start if not running
    help        - this screen
    
~]# systemctl status zabbix-agent
```
