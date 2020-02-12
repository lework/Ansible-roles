# Ansible Role: erlang

添加erlang环境

## 介绍

Erlang(['ə:læŋ])是一种通用的面向并发的编程语言，它由瑞典电信设备制造商爱立信所辖的CS-Lab开发，目的是创造一种可以应对大规模并发活动的编程语言和运行环境。Erlang问世于1987年，经过十年的发展，于1998年发布开源版本。Erlang是运行于虚拟机的解释性语言，但是现在也包含有乌普萨拉大学高性能Erlang计划（HiPE）开发的本地代码编译器，自R11B-4版本开始，Erlang也开始支持脚本式解释器。在编程范型上，Erlang属于多重范型编程语言，涵盖函数式、并发式及分布式。顺序执行的Erlang是一个及早求值, 单次赋值和动态类型的函数式编程语言。

官网: http://www.erlang.org/
官方文档: http://erlang.org/doc/man/erlang.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.9.1`

python `2.7.5`

os `Centos 7.4 X64` `Debian 9.4 X64` 

## 角色变量
```
software_files_path: "/opt/software"

erlang_version: "22.2"

erlang_file: "otp_src_{{ erlang_version }}.tar.gz"
erlang_file_path: "{{ software_files_path }}/{{ erlang_file }}"
erlang_file_url: "http://erlang.org/download/{{ erlang_file }}"


erlang_install_source: false
```

## 依赖

- gcc

## github地址
https://github.com/lework/Ansible-roles/tree/master/erlang

## Example Playbook
```yaml
# 默认安装
- hosts: node1
  roles:
    - erlang

# 指定版本安装
- hosts: node1
  roles:
    - { role: erlang, erlang_version: '22.2', erlang_install_source: true }
```