# Ansible Role: mycat

安装mycat

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    mycat_version: "1.6"

    mycat_file: "Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz"
    mycat_file_path: "{{ software_files_path }}/{{ mycat_file }}"
    mycat_file_url: "http://dl.mycat.io/1.6-RELEASE/Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz"
    mycat_conf_path: "{{ software_install_path }}/mycat/conf"
    
## 依赖

java

## github地址

https://github.com/kuailemy123/Ansible-roles/tree/master/mycat

## Example Playbook

    - hosts: servers
      roles:
        - mycat
