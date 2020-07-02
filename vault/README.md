# Ansible Role: vault

安装vault

## 介绍
Vault 是秘密访问私密信息的工具，可以帮你管理一些私密的信息，比如 API 密钥，密码，验证等等。Vault 提供一个统一的接口来访问所有隐私信息，同时提供严格的访问控制和记录详细的审计日志。

- 官方地址： https://www.vaultproject.io/
- 官方文档地址：https://www.vaultproject.io/docs
- Github: https://github.com/hashicorp/vault

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

vault_version: "1.4.2"

vault_file: "vault_{{ vault_version }}_linux_amd64.zip"
vault_file_path: "{{ software_files_path }}/{{ vault_file }}"
vault_file_url: "https://releases.hashicorp.com/vault/{{ vault_version }}/{{ vault_file }}"

vault_user: "vault"
vault_group: "vault"

vault_port: 8200
vault_cluster_port: 8201
vault_max_lease_ttl: "768h"
vault_default_lease_ttl: "768h"


vault_address: "0.0.0.0"
vault_protocol: "{% if vault_tls_disable %}http{% else %}https{% endif %}"

vault_cluster_address: "{{ ansible_default_ipv4.address }}"
vault_api_address: "{{ ansible_default_ipv4.address }}"

vault_cluster_addr: "{{ vault_protocol }}://{{ vault_cluster_address }}:{{ vault_cluster_port }}"
vault_api_addr: "{{ vault_protocol }}://{{ vault_api_address }}:{{ vault_port }}"

vault_cluster_disable: false


vault_bin_path: "/usr/local/sbin"
vault_home: "/vault_data"
vault_data_path: "{{ vault_home }}/data"
vault_config_path: "{{ vault_home }}/config"
vault_log_path: "{{ vault_home }}/log"
vault_plugin_path: "{{ vault_home }}/plugins"

vault_env_file: "/etc/profile.d/vault.sh"
vault_init_file: "~/vault.initkey"

# log
vault_log_level: "DEBUG"
vault_logrotate_freq: 7

vault_cluster_name: dc1
vault_ui: true
vault_audit_enable: true
vault_telemetry_enabled: false


# tls
vault_tls_disable: true
vault_tls_path: "{{ vault_home }}/ssl"
vault_tls_ca_file: ""
vault_tls_cert_file: ""
vault_tls_key_file: ""
vault_tls_require_and_verify_client_cert: false
vault_tls_disable_client_certs: false


# backend
vault_backend: raft

vault_backend_tls_enable: false
vault_backend_tls_cert_file: ""
vault_backend_tls_key_file: ""
vault_backend_tls_ca_file: ""

# vault
vault_vault: 127.0.0.1:8500
vault_vault_path: vault
vault_vault_service: vault
vault_vault_scheme: http
vault_vault_token:

# raft
vault_raft_node_id: "{{ ansible_hostname }}"
vault_raft_retry_join: []
  # - leader_api_addr:
  #   leader_ca_cert_file:
  #   leader_client_cert_file:
  #   leader_client_key_file:
```
## 依赖

## Github地址
https://github.com/lework/Ansible-roles/tree/master/vault

## Example Playbook

### 单机单实例

```yaml
---
- hosts: 192.168.77.131
  vars:
    - vault_backend: consul
    - vault_consul: "localhost:8500"
    - vault_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
  roles:
   - vault
```

### 三节点集群,后端使用raft

> `vault_cluster_addr`, `vault_api_addr` 时集群的`lb`地址, 不指定时使用各节点的ip地址

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - vault_cluster_addr: "http://192.168.77.140:8201"
    - vault_api_addr: "http://192.168.77.140:8200"
    - vault_backend: raft
    - vault_raft_retry_join:
        - leader_api_addr: http://192.168.77.131:8200
        - leader_api_addr: http://192.168.77.132:8200
        - leader_api_addr: http://192.168.77.133:8200
  roles:
   - vault
```

### 三节点集群,后端使用consul

> `vault_cluster_addr`, `vault_api_addr` 时集群的`lb`地址, 不指定时使用各节点的ip地址

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - vault_cluster_addr: "http://192.168.77.140:8201"
    - vault_api_addr: "http://192.168.77.140:8200"
    - vault_backend: consul
    - vault_consul: "localhost:8500"
    - vault_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
  roles:
   - vault
```

### 三节点集群,开启tls,后端使用raft

生成tls证书

```bash
curl -sSL https://cdn.jsdelivr.net/gh/lework/script@master/shell/cfssl.sh | bash -s - vault server.vault.com,192.168.77.131,192.168.77.132,192.168.77.133
```

> `vault_cluster_addr`, `vault_api_addr` 时集群的`lb`地址, 不指定时使用各节点的ip地址

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - vault_cluster_addr: "http://192.168.77.140:8201"
    - vault_api_addr: "http://192.168.77.140:8200"
    - vault_backend: raft
    - vault_raft_retry_join:
        - leader_api_addr: https://192.168.77.131:8200
          leader_ca_cert_file: "/vault_data/ssl/ca.pem"
          leader_client_cert_file: "/vault_data/ssl/server.pem"
          leader_client_key_file: "/vault_data/ssl/server-key.pem"
        - leader_api_addr: https://192.168.77.132:8200
          leader_ca_cert_file: "/vault_data/ssl/ca.pem"
          leader_client_cert_file: "/vault_data/ssl/server.pem"
          leader_client_key_file: "/vault_data/ssl/server-key.pem"
        - leader_api_addr: https://192.168.77.133:8200
          leader_ca_cert_file: "/vault_data/ssl/ca.pem"
          leader_client_cert_file: "/vault_data/ssl/server.pem"
          leader_client_key_file: "/vault_data/ssl/server-key.pem"
    - vault_tls_disable: false
    - vault_tls_ca_file: /opt/software/vault_ca/ca.pem
    - vault_tls_cert_file: /opt/software/vault_ca/server.pem
    - vault_tls_key_file: /opt/software/vault_ca/server-key.pem
  roles:
   - vault
```

### 三节点集群,开启tls,后端使用consul

> `vault_cluster_addr`, `vault_api_addr` 时集群的`lb`地址, 不指定时使用各节点的ip地址

```yaml
---
- hosts: 192.168.77.131,192.168.77.132,192.168.77.133
  vars:
    - vault_cluster_addr: "http://192.168.77.140:8201"
    - vault_api_addr: "http://192.168.77.140:8200"
    - vault_backend: consul
    - vault_consul: "localhost:8500"
    - vault_consul_token: "9f81839d-f906-8863-34a8-eb67ca2c25e3"
    - vault_tls_disable: false
    - vault_tls_ca_file: /opt/software/vault_ca/ca.pem
    - vault_tls_cert_file: /opt/software/vault_ca/server.pem
    - vault_tls_key_file: /opt/software/vault_ca/server-key.pem
  roles:
   - vault
```