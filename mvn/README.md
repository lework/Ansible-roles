# Ansible Role: mvn

添加mvn编译环境

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    mvn_version: "3.3.9"
    mvn_file: "apache-maven-{{ mvn_version }}-bin.tar.gz"
    mvn_file_path: "{{ software_files_path }}/{{ mvn_file }}"
    mvn_install_path: "{{ software_install_path }}/apache-maven-{{ mvn_version }}"
    mvn_file_url: "http://mirror.olnevhost.net/pub/apache/maven/maven-3/{{ mvn_version }}/binaries/apache-maven-{{ mvn_version }}-bin.tar.gz"

    link_force: false


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/mvn

## Example Playbook

    - hosts: servers
      roles:
        - mvn
    
    - hosts: servers
      roles:
        - { role: mvn, mvn_version: '3.2.5' }