# Ansible Role: java

添加jdk1.7版本

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	java_home: "/usr/java/jdk1.7.0_75"

	java_file: "jdk-7u75-linux-x64.gz"
	java_file_path: "{{ software_files_path }}/{{ java_file }}"
	java_install_path: "{{ software_install_path }}/jdk1.7.0_75"
	java_file_url: "http://download.oracle.com/otn-pub/java/jdk/7u75-b13/jdk-7u75-linux-x64.tar.gz"


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/java

## Example Playbook

    - hosts: servers
      roles:
        - java