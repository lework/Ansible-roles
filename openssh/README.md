# Ansible Role: openssh

安装 openssh

## 介绍
OpenSSH是使用SSH透过计算机网络加密通信的实现。它是取代由SSH Communications Security所提供的商用版本的开放源代码方案。当前OpenSSH是OpenBSD的子项目。

- 官方网站：https://www.openssh.com
- GitHub：https://github.com/openssl/openssl

## 要求

此角色在Debian和RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: 2.9.1
    os: Centos 7.4 X64
    python: 2.7.5

ansible管理主机

    os: Centos 6, Centos 7, Debian 9

## 角色变量

```yaml
software_files_path: "/opt/software"
software_install_path: "/usr"

openssh_version: "8.1p1"

openssh_file: "openssh-{{ openssh_version }}.tar.gz"
openssh_file_path: "{{ software_files_path }}/{{ openssh_file }}"
openssh_file_url: "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/{{ openssh_file }}"

openssh_ssl_dir: /usr/local/openssl

openssh_sshd_port: 22
openssh_sshd_use_dns: "no"
openssh_sshd_permit_root_login: "yes"
openssh_sshd_password_authentication: "yes"

```

## 依赖

- openssl

## github地址
https://github.com/lework/Ansible-roles/tree/master/openssh

## Example Playbook
```yaml
# 默认安装
- hosts: node1
  roles:
    - openssl
    - openssh

# 指定版本
- hosts: node1
  vars:
    - openssl_version: "1.1.1d"
    - openssh_version: "8.1p1"
  roles:
    - openssl
    - openssh
```
## 使用

```
ssh -V
```