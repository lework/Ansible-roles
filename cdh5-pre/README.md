# Ansible Role: cdh5 pre

安装cdh5时需要做的预处理操作.

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	cdh5_version: "5.11.0"
	cdh5_rpms_url: "http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/{{ cdh5_version }}/RPMS/x86_64"
	cdh5_jdk: "oracle-j2sdk1.7-1.7.0+update67-1.x86_64.rpm"
	cdh5_file_path: "{{ software_files_path }}/{{ cdh5_jdk }}"
	cdh5_jdk_url: "{{ cdh5_rpms_url }}/{{ cdh5_jdk }}"

	cdh5_java_home: "/usr/java/jdk1.7.0_67-cloudera"

	jdbc_version: "5.1.40"
	jdbc_file: "mysql-connector-java-{{ jdbc_version }}.tar.gz"
	jdbc_file_path: "{{ software_files_path }}/{{ jdbc_file }}"
	jdbc_jar_file: "mysql-connector-java-{{ jdbc_version}}/mysql-connector-java-{{ jdbc_version }}-bin.jar"
	jdbc_file_url: "http://101.96.10.44/dev.mysql.com/get/Downloads/Connector-J/{{ jdbc_file }}"


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/cdh5-pre

## Example Playbook

    - hosts: cdh5-all
      vars:
        - ipnames:
            '192.168.77.129': 'master'
            '192.168.77.130': 'node1'
            '192.168.77.131': 'node2'
      roles:
        - { role: cdh5-pre }
