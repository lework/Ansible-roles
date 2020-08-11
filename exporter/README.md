# Ansible Role: exporter

安装 prometheus 的 exporter，用于收集指标

## 介绍
exporter 可以将第三方系统中的现有指标导出为Prometheus指标。

官方地址： https://prometheus.io/
官方文档地址：https://prometheus.io/docs/instrumenting/exporters/

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

exporter_user: exporter
exporter_group: exporter

exporter_service_status: started
exporter_service_enabled: yes

exporter_name: "node_exporter"
exporter_conf_path: /etc/{{ exporter_name}}
exporter_conf_file: ""
```

node_exporter

```yaml
exporter_version: "1.0.1"
exporter_binary_file: node_exporter-{{ exporter_version }}.linux-amd64.tar.gz
exporter_binary_file_url: https://github.com/prometheus/node_exporter/releases/download/v{{ exporter_version }}/{{ exporter_binary_file }}

exporter_port: "9100"
exporter_log_level: "info"
exporter_web_listen_address: "0.0.0.0:{{ exporter_port }}"

exporter_config_flags_extra:
  log.level: "info"

exporter_conf: []

node_exporter_disabled_collectors: []
node_exporter_enabled_collectors: []
```

blackbox_exporter

```yaml
exporter_version: "0.17.0"
exporter_binary_file: blackbox_exporter-{{ exporter_version }}.linux-amd64.tar.gz
exporter_binary_file_url: https://github.com/prometheus/blackbox_exporter/releases/download/v{{ exporter_version }}/{{ exporter_binary_file }}

exporter_port: "9115"
exporter_web_listen_address: "0.0.0.0:{{ exporter_port }}"

exporter_config_flags_extra:
  log.level: "info"

exporter_conf:
  modules:
    http_2xx:
      prober: http
    http_post_2xx:
      prober: http
      http:
        method: POST
    tcp_connect:
      prober: tcp
    pop3s_banner:
      prober: tcp
      tcp:
        query_response:
        - expect: "^+OK"
        tls: true
        tls_config:
          insecure_skip_verify: false
    ssh_banner:
      prober: tcp
      tcp:
        query_response:
        - expect: "^SSH-2.0-"
    irc_banner:
      prober: tcp
      tcp:
        query_response:
        - send: "NICK prober"
        - send: "USER prober prober prober :prober"
        - expect: "PING :([^ ]+)"
          send: "PONG ${1}"
        - expect: "^:[^ ]+ 001"
    icmp:
      prober: icmp

```


## 依赖

None

## github地址
https://github.com/lework/Ansible-roles/tree/master/exporter

## Example Playbook

> 默认安装node_exporter

### 默认安装

```yaml
---

- hosts: node
  roles:
  - exporter
```

### 指定exporter


```yaml
---

- hosts: node
  vars:
    - exporter_name: blackbox_exporter
  roles:
    - exporter
```

### 指定配置

```yaml
---

- hosts: node
  vars:
    - exporter_name: blackbox_exporter
    - exporter_conf:
        modules:
          http_2xx_example:
            prober: http
            timeout: 5s
            http:
              valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
              valid_status_codes: []
              method: GET
  roles:
  - exporter
```

### 指定配置文件

```yaml
---

- hosts: node
  vars:
    - exporter_name: blackbox_exporter
    - exporter_conf_file: blackbox_exporter.yml
  roles:
  - exporter
```
