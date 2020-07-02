# Ansible Role: consul

安装consul

## 介绍
consul是HashiCorp公司推出的一款开源工具，用于实现分布式系统的服务发现与配置。与其他类似产品相比，提供更“一站式”的解决方案。consul内置有KV存储，服务注册/发现，健康检查，HTTP+DNS API，Web UI等多种功能。

- 官方地址： https://www.consul.io/
- 官方文档地址：https://www.consul.io/docs
- Github: https://github.com/hashicorp/consul

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

- ansible `2.9.10`
- os `Centos 7.7 X64`

## 角色变量
```yaml
software_files_path: "/opt/software"

consul_version: "1.8.0"

consul_file: "consul_{{ consul_version }}_linux_amd64.zip"
consul_file_path: "{{ software_files_path }}/{{ consul_file }}"
consul_file_url: "https://releases.hashicorp.com/consul/{{ consul_version }}/{{ consul_file }}"

consul_user: "consul"
consul_group: "consul"

consul_server_port: 8300
consul_http_port: 8500
consul_https_port: 8501
consul_dns_port: 8600
consul_ip_bind: "{{ ansible_default_ipv4.address }}"
consul_client_bind: "0.0.0.0"

consul_bin_path: "/usr/local/sbin"
consul_home: "/consul_data"
consul_data_path: "{{ consul_home }}/data"
consul_config_path: "{{ consul_home }}/config"
consul_log_path: "{{ consul_home }}/log"
consul_env_file: "/etc/profile.d/consul.sh"

# log
consul_log_file: "consul.log"
consul_log_level: "INFO"
consul_log_rotate_bytes: "52428800"
consul_log_rotate_duration: "24h"
consul_log_rotate_max_files: "7"
consul_syslog_enable: false
consul_syslog_facility: "local0"

consul_dc: "dc1"
consul_ui: true
consul_nodename: "{{ ansible_hostname }}"

consul_server: true
consul_retry_join: ["{{ consul_ip_bind }}"]
consul_bootstrap: false
consul_bootstrap_expect: "{{ consul_retry_join | length }}"
consul_encrypt: "{{ consul_retry_join | to_uuid | regex_replace('-', '') | b64encode }}"

# acl
consul_acl_enable: false
consul_acl_ttl: "30s"
consul_acl_token_persistence: true
consul_acl_down_policy: "extend-cache"
consul_acl_default_policy: "deny"
consul_acl_token: ""
consul_acl_agent_token: ""
consul_acl_agent_master_token: ""

# tls
consul_tls_enable: false
consul_tls_path: "{{ consul_home }}/ssl"
consul_tls_ca_crt: "consul-agent-ca.pem"
consul_tls_server_crt: "{{ consul_dc }}-server-consul-0.pem"
consul_tls_server_key: "{{ consul_dc }}-server-consul-0-key.pem"
consul_tls_client_crt: "{{ consul_dc }}-client-consul-0.pem"
consul_tls_client_key: "{{ consul_dc }}-client-consul-0-key.pem"
```
## 依赖

## Github地址
https://github.com/lework/Ansible-roles/tree/master/consul

## Example Playbook

### 单机单实例

```yaml
---
- hosts: node
  roles:
   - consul
   
# 开启tls
---
- hosts: node
  vars:
    - consul_tls_enable: true
  roles:
   - consul

# 开启acl
---
- hosts: node
  vars:
    - consul_acl_enable: true
  roles:
   - consul

# 开启tls 和acl
---
- hosts: node
  vars:
    - consul_tls_enable: true
    - consul_acl_enable: true
  roles:
   - consul
```

### 三节点集群

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - consul_retry_join: "{{ ansible_play_hosts }}"
  roles:
   - consul

# client
- hosts: 192.168.77.134
  vars:
   - consul_server: false
   - consul_retry_join:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
  roles:
   - consul
```

### 三节点集群, 开启tls

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - consul_retry_join: "{{ ansible_play_hosts }}"
    - consul_tls_enable: true
  roles:
   - consul

# client
- hosts: 192.168.77.134
  vars:
   - consul_server: false
   - consul_retry_join:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
   - consul_tls_enable: true
  roles:
   - consul
```

### 三节点集群, 开启acl

**安装server**

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - consul_retry_join: "{{ ansible_play_hosts }}"
    - consul_acl_enable: true
  roles:
   - consul
```

> 需记录下输出的 token 信息

**安装client**

> `consul_acl_agent_token` 使用上面的客户端 `token`

```yaml

- hosts: 192.168.77.134
  vars:
   - consul_server: false
   - consul_retry_join:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
   - consul_acl_enable: true
   - consul_acl_agent_token: "76d432af-a085-15bd-ecbe-9435dadfea95"
  roles:
   - consul
```

### 三节点集群, 开启acl和tls

**安装server**

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - consul_retry_join: "{{ ansible_play_hosts }}"
    - consul_acl_enable: true
    - consul_tls_enable: true
  roles:
   - consul
```

> 需记录下输出的 token 信息

**安装client**

> `consul_acl_agent_token` 使用上面的客户端 `token`

```yaml
- hosts: 192.168.77.134
  vars:
   - consul_server: false
   - consul_retry_join:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
   - consul_acl_enable: true
   - consul_acl_agent_token: "d20a5a12-7d6b-c589-43f6-655df849eefc"
   - consul_tls_enable: true
  roles:
   - consul
```



