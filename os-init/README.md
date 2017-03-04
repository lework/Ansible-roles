# Ansible Role: OS INIT

安装CentOS系统后，进行一些初始化操作。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
无

## 初始化项目

1. ntp同步时间
2. 修改nofile limits
3. 关闭selinux
4. 关闭transparent hugepage
5. 关闭iptables
6. 安装gcc
7. 设置vm.overcommit_memory 为1
8. 设置vm.swappiness 为1
9. update bash


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/os-init

## Example Playbook

    - hosts: servers
      roles:
        - os-init