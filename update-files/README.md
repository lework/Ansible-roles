# Ansible Role: update-files

update-files

## 介绍

update-files 是用来更新应用的配置文件

## 要求

此角色仅在RHEL或Debian及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量

```yaml
---
# author: lework

# 源目录
src_path: ""

# 目标目录
dest_path: ""

# 文件权限
file_user: root
file_group: root
file_mode: '0644'

# 应用重载
reload_app: nginx
```

## 依赖

## github地址
https://github.com/lework/Ansible-roles/tree/master/update-files

## Example Playbook

### 更新证书文件

```yaml
---

- hosts: localhost
  remote_user: root
  gather_facts: no
  roles:
    - role: update-files
      src_path: /etc/ansible/certs
      dest_path: /etc/nginx/ssl
      reload_app: nginx

    - role: update-files
      src_path: /etc/ansible/certs
      dest_path: /etc/haproxy/ssl
      reload_app: haproxy
```