# Ansible Role: cdh5 agent

安装cdh5 agent

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
	software_files_path: "/opt/software"

	cdh5_version: "5.11.0"
	cdh5_rpms_url: "http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/{{ cdh5_version }}/RPMS/x86_64"

	cdh5_cm_daemons: "cloudera-manager-daemons-5.11.0-1.cm5110.p0.101.el6.x86_64.rpm"
	cdh5_cm_daemons_url: "{{ cdh5_rpms_url }}/{{ cdh5_cm_daemons }}"

	cdh5_cm_agent: "cloudera-manager-agent-5.11.0-1.cm5110.p0.101.el6.x86_64.rpm"
	cdh5_cm_agent_url: "{{ cdh5_rpms_url }}/{{ cdh5_cm_agent }}"

	cdh5_server_host: 'localhost'


## 依赖

cdh5-pre

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/cdh5-agent

## Example Playbook

    - hosts: cdh5-agent
      vars:
        - cdh5_server_host: '192.168.77.129'
      roles:
        - { role: cdh5-agent }
	   
## 使用

```
# service cloudera-scm-agent 
Usage: cloudera-scm-agent {start|stop|restart|clean_start|hard_stop|hard_restart|clean_restart|status|condrestart}
```