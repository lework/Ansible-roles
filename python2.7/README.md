# Ansible Role: python2.7

Centos 6.7版本中的python2.6升级到2.7

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software/"
    software_install_path: "/usr/local"

    python_version: "2.7.13"

    python_file: "Python-{{ python_version }}.tgz"
    python_file_path: "{{ software_files_path }}/{{ python_file }}"
    python_file_url: "http://www.python.org/ftp/python/{{ python_version }}/Python-{{ python_version }}.tgz"

    pip_source_url: "https://pypi.tuna.tsinghua.edu.cn/simple"
    change_pip_source: true


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/python2.7

## Example Playbook

    - hosts: servers
      roles:
        - python2.7
        
    - hosts: server
      roles:
        - { role: python2.7, python_version: "2.7.13"}