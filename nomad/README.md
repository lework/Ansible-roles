# Ansible Role: nomad

安装nomad

## 介绍
Nomad 是一个集群管理器和调度器，专为微服务和批量处理工作流设计。Nomad 是分布式，高可用，可扩展到跨数据中心和区域的数千个节点。

- 官方地址： https://www.nomadproject.io
- 官方文档地址：https://www.nomadproject.io/docs
- github: https://github.com/hashicorp/nomad

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

- ansible `2.9.10`
- os `Centos 7.7 X64`

## 角色变量
```yaml
---
# author: lework

software_files_path: "/opt/software"

nomad_version: "0.11.3"

nomad_file: "nomad_{{ nomad_version }}_linux_amd64.zip"
nomad_file_path: "{{ software_files_path }}/{{ nomad_file }}"
nomad_file_url: "https://releases.hashicorp.com/nomad/{{ nomad_version }}/{{ nomad_file }}"

nomad_http_port: 4646
nomad_rpc_port: 4647
nomad_serf_port: 4648
nomad_bind_addr: "{{ ansible_default_ipv4.address }}"
nomad_advertise_addr: "{{ ansible_default_ipv4.address }}"

# path
nomad_bin_path: "/usr/local/sbin"
nomad_home: "/nomad_data"
nomad_data_path: "{{ nomad_home }}/data"
nomad_config_path: "{{ nomad_home }}/config"
nomad_log_path: "{{ nomad_home }}/log"
nomad_plugin_path: "{{ nomad_home }}/plugin"
nomad_env_file: "/etc/profile.d/nomad.sh"

nomad_datacenter: "dc1"
nomad_region: "global"
nomad_log_level: "INFO"
nomad_syslog_enable: true
nomad_node_name: "{{ ansible_hostname }}"
nomad_debug: false

nomad_log_json: false
nomad_log_file: "{{ nomad_log_path }}/nomad.log"
nomad_log_rotate_bytes: 104857600
nomad_log_rotate_duration: "24h"
nomad_log_rotate_max_files: 10

nomad_server: true
nomad_retry_join: ["127.0.0.1"]

nomad_client: false
nomad_client_servers: ["127.0.0.1"]

nomad_bootstrap: false
nomad_bootstrap_expect: "{{ nomad_retry_join | length }}"
nomad_encrypt: "{{ nomad_retry_join | to_uuid | regex_replace('-', '') | b64encode }}"

# acl
nomad_acl_enable: false
nomad_acl_token_ttl: "30s"
nomad_acl_policy_ttl: "30s"
nomad_acl_replication_token: ""

# tls
nomad_tls_enable: false
nomad_tls_path: "{{ nomad_home }}/ssl"
nomad_tls_ca_file: ""
nomad_tls_cert_file: ""
nomad_tls_key_file: ""
nomad_tls_verify_server_hostname: true
nomad_tls_verify_https_client: true

# consul
nomad_consul_enable: false
nomad_consul_address: "localhost:8500"
nomad_consul_token: ""
nomad_consul_servers_service_name: "nomad-servers"
nomad_consul_clients_service_name: "nomad-clients"
nomad_consul_tags: {}

# telemetry
nomad_telemetry_enable: true
```
## 依赖

## Github地址
https://github.com/lework/Ansible-roles/tree/master/nomad

## Example Playbook

### 单机单实例

```yaml
---
- hosts: node
  vars:
    - nomad_server: true
    - nomad_client: true
  roles:
   - nomad
```

### 三节点集群

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - nomad_retry_join: "{{ ansible_play_hosts }}"
  roles:
   - nomad

# client
- hosts: 192.168.77.134
  vars:
   - nomad_server: false
   - nomad_client: true
   - nomad_client_servers:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
  roles:
   - nomad
```

### 三节点集群, 使用consul

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - nomad_retry_join: "{{ ansible_play_hosts }}"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
  roles:
   - nomad

# client
- hosts: 192.168.77.134
  vars:
    - nomad_server: false
    - nomad_client: true
    - nomad_client_servers:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
  roles:
   - nomad
```

### 三节点集群, 开启acl

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - nomad_retry_join: "{{ ansible_play_hosts }}"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
    - nomad_acl_enable: true
  roles:
   - nomad

# client
- hosts: 192.168.77.134
  vars:
    - nomad_server: false
    - nomad_client: true
    - nomad_client_servers:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
    - nomad_acl_enable: true
  roles:
   - nomad
```

### 三节点集群, 开启tls

生成证书
```bash
curl -sSL https://cdn.jsdelivr.net/gh/lework/script@master/shell/cfssl.sh | bash -s - vault server.global.nomad client.global.nomad
```

```yaml
---
# server
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - nomad_retry_join: "{{ ansible_play_hosts }}"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
    - nomad_tls_enable: true
    - nomad_tls_ca_file: "/opt/software/nomad_ca/ca.pem"
    - nomad_tls_cert_file: "/opt/software/nomad_ca/server.pem"
    - nomad_tls_key_file: "/opt/software/nomad_ca/server-key.pem"
  roles:
   - nomad

# client
- hosts: 192.168.77.134
  vars:
    - nomad_server: false
    - nomad_client: true
    - nomad_client_servers:
       - "192.168.77.131"
       - "192.168.77.132"
       - "192.168.77.133"
    - nomad_consul_enable: true
    - nomad_consul_address: "localhost:8500"
    - nomad_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
    - nomad_tls_enable: true
    - nomad_tls_ca_file: "/opt/software/nomad_ca/ca.pem"
    - nomad_tls_cert_file: "/opt/software/nomad_ca/client.pem"
    - nomad_tls_key_file: "/opt/software/nomad_ca/client-key.pem"
  roles:
   - nomad
```