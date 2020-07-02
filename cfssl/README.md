# Ansible Role: cfssl

安装cfssl

## 介绍
CFSSL是CloudFlare开源的一款PKI/TLS工具。 CFSSL 包含一个命令行工具 和一个用于 签名，验证并且捆绑TLS证书的 HTTP API 服务。 使用Go语言编写。

- Github 地址： https://github.com/cloudflare/cfssl
- 官网: https://cfssl.org/
- 下载包地址： https://pkg.cfssl.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

- ansible `2.9.10`
- os `Centos 7.7 X64`

## 角色变量
```yaml
software_files_path: "/opt/software"

cfssl_version: "1.4.1"

cfssl_pkg:
  cfssl:
    path: "{{ software_files_path }}/cfssl"
    url: "https://github.com/cloudflare/cfssl/releases/download/v{{ cfssl_version }}/cfssl_{{ cfssl_version }}_linux_amd64"
  cfssljson:
    path: "{{ software_files_path }}/cfssljson"
    url: "https://github.com/cloudflare/cfssl/releases/download/v{{ cfssl_version }}/cfssljson_{{ cfssl_version }}_linux_amd64"

cfssl_download_list:
  - "{{ cfssl_pkg.cfssl }}"
  - "{{ cfssl_pkg.cfssljson }}"

cfssl_bin_path: "/usr/local/sbin"

cfssl_project: "example"
cfssl_server_hostname: "server.example.com"
cfssl_client_hostname: "client.example.com"

cfssl_data_path: "/cfssl_data"
cfssl_ca_path: "{{ cfssl_data_path}}/{{ cfssl_project }}"

cfssl_ca_expiry: 87600h # 10 year
cfssl_key_algo: "ecdsa"
cfssl_key_size: 256
    
    
cfssl_cert: true
```
## 依赖

## Github地址
https://github.com/lework/Ansible-roles/tree/master/cfssl

## Example Playbook

### 默认安装部署和生成签名证书

```yaml
---
- hosts: node
  roles:
   - cfssl
```
### 默认安装部署，不生成签名证书
```yaml
---
- hosts: node
  vars:
    - cfssl_cert: false
  roles:
   - cfssl
```