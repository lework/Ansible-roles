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

- ansible `2.9.1`
- os `Centos 7.4 X64`

## 角色变量
```yaml
---
# pip 国内源
supervisor_package_index: https://pypi.tuna.tsinghua.edu.cn/simple

# supervisor版本, 默认是最新版本
supervisor_version: null
supervisor_pip_package: 
  - "{%if ansible_python.version.major == 3%}python3-pip{%else%}python-pip{%endif%}"

# supervisor的依赖包
supervisor_supervisor_package:
  - name: supervisor
    version: "{% if not supervisor_version and ansible_python.version.major == 2 and ansible_python.version.micro < 7 %}3.4.0{%else%}{{supervisor_version}}{%endif%}"
  - "{%- if ansible_python.version.major == 2 and ansible_python.version.micro < 7 -%}{{ '{\"name\": \"meld3\", \"version\": \"0.6.10\"}' | from_json }}{%- endif -%}"

# 是否启动supervisor
supervisor_started: true
supervisor_enabled: true

supervisor_config_path: /etc/supervisor
supervisor_log_path: /var/log/supervisor

supervisor_nodaemon: false

# supervisor的运行用户和密码
supervisor_user: root
supervisor_password: ''

# socket方式
supervisor_unix_http_server_enable: true
supervisor_unix_http_server_socket_path: /var/run/supervisor.sock

# http方式
supervisor_inet_http_server_enable: false
supervisor_inet_http_server_port: '127.0.0.1:9001'

# 定义supervisor管理的program
supervisor_programs: []
# - name: 'example'
#   command: java -jar /tmp/example.jar
# - name: 'apache'
#   command: apache2ctl -c "ErrorLog /dev/stdout" -DFOREGROUND
#   configuration: |
#     autostart=true
#     autorestart=true
#     startretries=1
#     startsecs=1
#     redirect_stderr=true
#     stderr_logfile=/var/log/apache-err.log
#     stdout_logfile=/var/log/apache-out.log
#     user=root
#     killasgroup=true
#     stopasgroup=true

# 开启supervisor的健康检查, 详细config见脚本
supervisor_healthCheck_enable: false
supervisor_healthCheck_config: |
    config:
      # supervisordUrl: http://localhost:9001/RPC2
      mail:
        # host: 'smtp.test.com'
        # port: '465'
        # user: 'ops@test.com'
        # pass: '123415'
        # to_list: ['test@test.com']
      wechat:
        corpid: ""
        secret: ""
        agentid: ""
        toparty: ""
    example:
      type: HTTP
      method: GET
      host: 127.0.0.1
      port: 80
      path: /test
      periodSeconds: 5
      timeoutSeconds: 5
      failureThreshold: 2
      successThreshold: 1
      action: restart,wechat

# 开启supervisor的Prometheus的metrics指标
supervisor_exporter_enable: false
supervisor_exporter_port: 8081

```
    

## 依赖

- facts
- epel
- pip
- python

## github地址
https://github.com/lework/Ansible-roles/tree/master/supervisor

## Example Playbook
```yaml
# 默认安装
- hosts: node1
  roles:
   - supervisor
   
# 定义supervisor管理的program
- hosts: node1
  vars:
    - supervisor_unix_http_server_enable: false
    - supervisor_inet_http_server_enable: true
    - supervisor_programs:
       - name: 'example'
         command: python -m SimpleHTTPServer
       - name: 'example2'
         command: python -m SimpleHTTPServer 8082
         configuration: |
           process_name=%(program_name)s
           numprocs=1
           autostart=true
           startsecs=2
           startretries=5
           autorestart=true
           stopsignal=TERM
           stopwaitsecs=3
           stopasgroup=true
           killasgroup=true
           user=root
           redirect_stderr=true
           stdout_logfile=/var/log/supervisor/example2.log
           stdout_logfile_maxbytes=200MB
           stdout_logfile_backups=10
  roles:
   - supervisor

# 开启supervisor的健康检查和metrics指标
- hosts: node1
  vars:
    - supervisor_password: 123456
    - supervisor_unix_http_server_enable: ture
    - supervisor_inet_http_server_enable: false
    - supervisor_programs:
       - name: 'example'
         command: python -m SimpleHTTPServer
       - name: 'example2'
         command: python -m SimpleHTTPServer 8082
         configuration: |
           process_name=%(program_name)s
           numprocs=1
           autostart=true
           startsecs=2
           startretries=5
           autorestart=true
           stopsignal=TERM
           stopwaitsecs=3
           stopasgroup=true
           killasgroup=true
           user=root
           redirect_stderr=true
           stdout_logfile=/var/log/supervisor/example2.log
           stdout_logfile_maxbytes=200MB
           stdout_logfile_backups=10
    - supervisor_healthCheck_enable: true
    - supervisor_healthCheck_config: |
        config:
          supervisordUrl: unix:///var/run/supervisor.sock
          supervisordUser: root
          supervisordPass: 123456
          mail:
            host: 'smtp.test.com'
            port: '465'
            user: 'ops@test.com'
            pass: '123456'
            to_list: ['test@test.com']
          wechat:
            corpid: ""
            secret: ""
            agentid: ""
            touser: ""
        example:
          type: HTTP
          method: GET
          host: 127.0.0.1
          port: 8000
          path: /
          periodSeconds: 5
          timeoutSeconds: 5
          failureThreshold: 2
          successThreshold: 1
          action: restart,wechat
          sendResolved: True
        example2:
          type: HTTP
          method: GET
          host: 127.0.0.1
          port: 8082
          path: /
          periodSeconds: 5
          timeoutSeconds: 5
          failureThreshold: 2
          successThreshold: 1
          action: restart,email
          sendResolved: True
    - supervisor_exporter_enable: true
    - supervisor_exporter_port: 8081
  roles:
   - supervisor
```
    
## 使用

```bash
supervisord -v
supervisorctl status
supervisorctl stop example
supervisorctl start example

#systemd
systemctl status supervisord
systemctl start supervisord
systemctl stop supervisord
systemctl reload supervisord

#non-systemd 
/etc/init.d/supervisord status
/etc/init.d/supervisord start
/etc/init.d/supervisord stop
```

- supervisor:
  - [conf] `/etc/supervisord.conf`
  - [log] ` /var/log/supervisor/`

- exporter: 
  - [http] `http://node1:8081/metrics`
  - [script] `/etc/supervisord.d/scripts/supervisor_exporter.py`
- healthCheck: 
  - [script] `/etc/supervisord.d/scripts/healthCheck.py`
  - [config] `/etc/supervisord.d/scripts/config.yaml`
  - [log] `/var/log/supervisor/healthCheck.log` 
  