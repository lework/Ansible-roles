# Ansible Role: openssl

安装 openssl

## 介绍
在计算机网络上，OpenSSL是一个开放源代码的软件库包，应用程序可以使用这个包来进行安全通信，避免窃听，同时确认另一端连线者的身份。这个包广泛被应用在互联网的网页服务器上。 其主要库是以C语言所写成，实现了基本的加密功能，实现了SSL与TLS协议。

- 官方网站：https://www.openssl.org
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
software_install_path: "/usr/local/openssl"

openssl_version: "1.1.1d"

openssl_file: "openssl-{{ openssl_version }}.tar.gz"
openssl_file_path: "{{ software_files_path }}/{{ openssl_file }}"
openssl_file_url: "https://www.openssl.org/source/{{ openssl_file }}"

```

## 依赖


## github地址
https://github.com/lework/Ansible-roles/tree/master/openssl

## Example Playbook
```yaml
# 默认安装
- hosts: node1
  roles:
    - openssl

# 指定版本
- hosts: node1
  vars:
    - openssl_version: "1.1.1d"
  roles:
    - openssl
```
## 使用

```
openssl version
```