# Ansible Role: ssh-2fa

开启 SSH 的双因子认证登录

## 介绍

使用 Google Authenticator 来实现 SSH 的双因子认证登录

- 官方网站：https://github.com/google/google-authenticator-libpam

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

google_authenticator_version: "1.08"

google_authenticator_file: "google-authenticator-libpam-{{ google_authenticator_version }}.tar.gz"
google_authenticator_file_path: "{{ software_files_path }}/{{ google_authenticator_file }}"
google_authenticator_file_url: "https://github.com/google/google-authenticator-libpam/archive/{{ google_authenticator_version }}.tar.gz"

google_authenticator_step_size: 30
google_authenticator_rate_limit: 3
google_authenticator_rate_time: 30

google_authenticator_command: | 
  google-authenticator \
  --time-based \
  --step-size={{ google_authenticator_step_size }} \
  --rate-limit={{ google_authenticator_rate_limit }} \
  --rate-time={{ google_authenticator_rate_time }} \
  --minimal-window \
  --disallow-reuse \
  --force \
  --quiet
google_authenticator_user: "{{ ansible_user_id | d('root')}}"

google_authenticator_pam: /usr/local/lib/security/pam_google_authenticator.so
```
    
## 依赖

- chrony

## github地址
https://github.com/lework/Ansible-roles/tree/master/ssh-2fa

## Example Playbook

```yaml
# 默认安装
- hosts: node1
  roles:
    - chrony
    - ssh-2fa

# 指定认证的用户
- hosts: node1
  vars:
    google_authenticator_user: test
  roles:
    - chrony
    - ssh-2fa
```