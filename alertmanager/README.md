# Ansible Role: alertmanager

安装alertmanager，用于接受和发送报警信息

## 介绍
Prometheus服务器中的警报规则向Alertmanager发送警报。Alertmanager然后管理这些警报，包括静默、抑制、聚合，以及通过电子邮件、随叫随到的通知系统和聊天平台发送通知。

github: https://github.com/prometheus/alertmanager
官方文档地址：https://prometheus.io/docs/alerting/latest/overview/

## 要求

此角色仅在RHEL或Debian及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量
```yaml
software_files_path: "/opt/software"
software_install_path: "/usr/local"

alertmanager_version: "0.21.0"
alertmanager_binary_file: alertmanager-{{ alertmanager_version }}.linux-amd64.tar.gz
alertmanager_binary_file_url: https://github.com/alertmanager/alertmanager/releases/download/v{{ alertmanager_version }}/{{ alertmanager_binary_file }}

alertmanager_user: alertmanager
alertmanager_group: alertmanager

alertmanager_service_status: started
alertmanager_service_enabled: yes

alertmanager_conf_path: /etc/alertmanager
alertmanager_templates_path: "{{ alertmanager_conf_path }}/templates"
alertmanager_db_path: /var/lib/alertmanager

alertmanager_port: "9093"
alertmanager_web_listen_address: "0.0.0.0:{{ alertmanager_port }}"
alertmanager_web_external_url: ''

alertmanager_config_flags_extra:
  log.level: info

alertmanager_cluster: {}
# alertmanager_cluster:
#    listen-address: "{{ ansible_default_ipv4.address }}:6783"
#    peers:
#      - "{{ ansible_default_ipv4.address }}:6783"


alertmanager_conf:
  global:
    resolve_timeout: 5m
  route:
    group_by: ['alertname']
    group_wait: 10s
    group_interval: 10s
    repeat_interval: 1h
    receiver: 'web.hook'
  receivers:
  - name: 'web.hook'
    webhook_configs:
    - url: 'http://127.0.0.1:5001/'
  inhibit_rules:
    - source_match:
        severity: 'critical'
      target_match:
        severity: 'warning'
      equal: ['alertname', 'dev', 'instance']

alertmanager_conf_file: ""
alertmanager_template_files: []
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/alertmanager

## Example Playbook

### 默认安装

```yaml
---

- hosts: node
  roles:
  - alertmanager
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - alertmanager_conf:
        global:
          smtp_smarthost: 'smtp.test.com:25'
          smtp_from: 'lework@test.com'
          smtp_auth_username: 'lework@test.com'
          smtp_auth_password: '<password>'
        templates: 
        - '/etc/alertmanager/template/*.tmpl'
        route:
          group_by: ['alertname']
          group_wait: 5s
          group_interval: 5s
          repeat_interval: 1h
          receiver: default-receiver
        receivers:
        - name: 'default-receiver'
          email_configs:
          - to: 'lework@test.com'
            send_resolved: true
  roles:
  - alertmanager
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - alertmanager_conf_file: alertmanager-conf.yml
  roles:
  - alertmanager
```

### 集群配置

```yaml
---

- hosts: node1 node2 node3
  vars:
    - alertmanager_cluster:
        listen-address: "{{ ansible_default_ipv4.address }}:6783"
        peers:
          - "node1:6783"
          - "node2:6783"
          - "node3:6783"
  roles:
  - alertmanager
```