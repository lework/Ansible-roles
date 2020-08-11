# Ansible Role: pushgateway

安装pushgateway，用于接受指标

## 介绍
Prometheus Pushgateway的存在是为了允许临时作业和批处理作业向Prometheus公开其指标。 由于这些工作可能存在的时间不够长，因此它们可以将其指标推送到Pushgateway。 然后，Pushgateway将这些指标公开给Prometheus。

github: https://github.com/prometheus/pushgateway

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

pushgateway_version: "1.2.0"
pushgateway_binary_file: pushgateway-{{ pushgateway_version }}.linux-amd64.tar.gz
pushgateway_binary_file_url: https://github.com/prometheus/pushgateway/releases/download/v{{ pushgateway_version }}/{{ pushgateway_binary_file }}

pushgateway_user: pushgateway
pushgateway_group: pushgateway

pushgateway_service_status: started
pushgateway_service_enabled: yes

pushgateway_persistence: true
pushgateway_persistence_path: /var/lib/pushgateway

pushgateway_port: "9091"
pushgateway_web_listen_address: "0.0.0.0:{{ pushgateway_port }}"
pushgateway_web_external_url: ''

pushgateway_config_flags_extra:
  log.level: info
```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/pushgateway

## Example Playbook

### 默认安装

```yaml
---

- hosts: node
  roles:
  - pushgateway
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - pushgateway_port: 19091
    - pushgateway_config_flags_extra:
        log.level: debug
        log.format: json
  roles:
  - pushgateway
```