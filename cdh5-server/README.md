# Ansible Role: cdh5 server

只安装cdh5 server服务，不安装hadoop集群。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
	software_files_path: "/opt/software"

	cdh5_version: "5.11.0"
	cdh5_rpms_url: "http://archive.cloudera.com/cm5/redhat/6/x86_64/cm/{{ cdh5_version }}/RPMS/x86_64"

	cdh5_cm_daemons: "cloudera-manager-daemons-5.11.0-1.cm5110.p0.101.el6.x86_64.rpm"
	cdh5_cm_daemons_url: "{{ cdh5_rpms_url }}/{{ cdh5_cm_daemons }}"

	cdh5_cm_server: "cloudera-manager-server-5.11.0-1.cm5110.p0.101.el6.x86_64.rpm"
	cdh5_cm_server_url: "{{ cdh5_rpms_url }}/{{ cdh5_cm_server }}"

	cdh5_parcels_url: "http://archive.cloudera.com/cdh5/parcels/{{ cdh5_version }}"

	cdh5_parcels_cdh: "CDH-5.11.0-1.cdh5.11.0.p0.34-el6.parcel"
	cdh5_parcels_cdh_url: "{{ cdh5_parcels_url }}/{{ cdh5_parcels_cdh }}"

	cdh5_parcels_cdh_sha: "CDH-5.11.0-1.cdh5.11.0.p0.34-el6.parcel.sha1"
	cdh5_parcels_cdh_sha_url: "{{ cdh5_parcels_url }}/{{ cdh5_parcels_cdh_sha }}"

	cdh5_parcels_manifest: "manifest.json"
	cdh5_parcels_manifest_url: "{{ cdh5_parcels_url }}/{{ cdh5_parcels_manifest }}"

	jdbc_version: "5.1.40"
	jdbc_file: "mysql-connector-java-{{ jdbc_version }}.tar.gz"
	jdbc_file_path: "{{ software_files_path }}/{{ jdbc_file }}"
	jdbc_jar_file: "mysql-connector-java-{{ jdbc_version}}/mysql-connector-java-{{ jdbc_version }}-bin.jar"
	jdbc_file_url: "http://101.96.10.44/dev.mysql.com/get/Downloads/Connector-J/{{ jdbc_file }}"

	cmf_db_host: "{{ mysql_host | default('localhost') }}"
	cmf_db_port: "{{ mysql_port | default('3306') }}"
	cmf_db_name: 'cmf'
	cmf_db_user: 'cmf'
	cmf_db_pass: '123456'

	hive_db_name: 'hive'
	hive_db_user: 'hive'
	hive_db_pass: '123456'

	amon_db_name: 'amon'
	amon_db_user: 'amon'
	amon_db_pass: '123456'

	hue_db_name: 'hue'
	hue_db_user: 'hue'
	hue_db_pass: '123456'

	oozie_db_name: 'oozie'
	oozie_db_user: 'oozie'
	oozie_db_pass: '123456'

## 依赖

cdh5-pre
cdh5-agent

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/cdh5-server

## Example Playbook

    - hosts: cdh5-server
      vars:
        - mysql_host: 192.168.77.129
        - mysql_user: root
        - mysql_password: 123456
        - mysql_binlog_format: 'MiXED'
      roles: 
        - { role: mysql }
        - { role: cdh5-server }

## 使用

命令使用

```
# service cloudera-scm-server
Usage: cloudera-scm-server {start|force_start|stop|restart|status|condrestart}

```

web 使用

http://master:7180/cmf/login

默认用户名/密码: admin/admin

然后跟着web页面一步一步的部署hadoop集群