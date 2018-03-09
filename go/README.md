# Ansible Role: go

添加go开发环境

## 介绍

Go是一种编译型语言，它结合了解释型语言的游刃有余，动态类型语言的开发效率，以及静态类型的安全性。它也打算成为现代的，支持网络与多核计算的语言。要满足这些目标，需要解决一些语言上的问题：一个富有表达能力但轻量级的类型系统，并发与垃圾回收机制，严格的依赖规范等等。这些无法通过库或工具解决好，因此Go也就应运而生了。

官网: https://golang.org

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

    go_version: "1.10"
    go_file: "go{{ go_version }}.linux-amd64.tar.gz"
    go_file_path: "{{ software_files_path }}/{{ go_file }}"
    go_file_url: "https://studygolang.com/dl/golang/{{ go_file }}"

## 依赖

gcc

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/go

## Example Playbook

    - hosts: node1
      roles:
        - go
	
    - hosts: node1
      roles:
        - { role: go, go_version: '1.9.4' }