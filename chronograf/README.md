# Ansible Role: chronograf

安装chronograf

## 介绍
Chronograf是InfluxData的开源Web应用程序。 将Chronograf与TICK堆栈的其他组件结合使用，可以直观地显示监视数据并轻松创建警报和自动化规则。

官方地址： https://www.influxdata.com/time-series-platform/chronograf/
github: https://github.com/influxdata/chronograf
官方文档地址：https://docs.influxdata.com/chronograf/

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

chronograf_version: "1.8.6"


# Service
chronograf_service_status: started
chronograf_service_enabled: yes

# Port
chronograf_port: 8888
```

发行版变量

```yaml

# Debian.yml
__package_file: chronograf_{{ chronograf_version }}_amd64.deb
__package_file_url: https://dl.influxdata.com/chronograf/releases/{{ __package_file }}


# RedHat.yml
__package_file: chronograf-{{ chronograf_version }}.x86_64.rpm
__package_file_url: https://dl.influxdata.com/chronograf/releases/{{ __package_file }}

```

## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/chronograf

## Example Playbook

> 默认使用package包方式安装

### 默认安装

```yaml
---

- hosts: node
  roles:
  - chronograf
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - chronograf_port: 8080
  roles:
  - chronograf
```
