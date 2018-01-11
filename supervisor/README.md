# Ansible Role: supervisor

安装supervisor

## 介绍
Supervisor是一个进程监控程序。

满足的需求是：我现在有一个进程需要每时每刻不断的跑，但是这个进程又有可能由于各种原因有可能中断。当进程中断的时候我希望能自动重新启动它，此时，我就需要使用到了Supervisor.

Supervisor的两个命令:
supervisord： supervisor的服务器端部分，启动supervisor就是运行这个命令
supervisorctl：启动supervisor的命令行窗口。


github地址： https://github.com/Supervisor/supervisor
官方文档地址：http://supervisord.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    supervisor_conf_path: "/etc/supervisor"
    supervisor_run_path: "/var/run/supervisor"
    supervisor_log_path: "/var/log/supervisor"

    supervisor_bin: "/usr/bin/supervisorctl"

    supervisor_env: ""
    supervisor_stopsignal: "TERM"
    supervisor_program: []
    # [{ name: 'superset', command: '/usr/local/bin/superset runserver', user: 'superset' }]
    

## 依赖

python2.7
pip

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/supervisor

## Example Playbook

    - hosts: node1
      vars:
        supervisor_name: superset
        supervisor_program: 
          - { name: 'superset', command: '/usr/local/bin/superset runserver', user: 'superset' }
      roles:
       - { role: python2.7 }
       - { role: supervisor }
    