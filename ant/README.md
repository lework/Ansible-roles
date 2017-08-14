# Ansible Role: ant

添加ant编译环境

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.1.0`
os `Centos 6.7 X64`

## 角色变量
    ant_version: "1.10.1"
    ant_file: "apache-ant-{{ ant_version }}-bin.tar.gz"
    ant_file_path: "{{ software_files_path }}/{{ ant_file }}"
    ant_install_path: "{{ software_install_path }}/apache-ant-{{ ant_version }}"
    ant_file_url: "http://mirrors.tuna.tsinghua.edu.cn/apache//ant/binaries/{{ ant_file }}"

    ivy_version: "2.4.0"
    ivy_file: "ivy-{{ ivy_version }}.jar"
    ivy_file_path: "{{ software_files_path }}/{{ ivy_file }}"
    ivy_file_url: "http://repo1.maven.org/maven2/org/apache/ivy/ivy/{{ ivy_version }}/{{ ivy_file }}"

## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/ant

## Example Playbook

    - hosts: node1
      roles:
        - ant