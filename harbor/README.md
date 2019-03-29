# Ansible Role: harbor

安装harbor

## 介绍
　　Harbor是一个用于存储和分发Docker镜像的企业级Registry服务器,通过添加一些企业必需的功能特性,例如安全、标识和管理等,扩展了开源Docker Distribution。作为一个企业级私有Registry服务器,Harbor提供了更好的性能和安全。提升用户使用Registry构建和运行环境传输镜像的效率。Harbor支持安装在多个Registry节点的镜像资源复制,镜像全部保存在私有Registry中, 确保数据和知识产权在公司内部网络中管控。另外,Harbor也提供了高级的安全特性,诸如用户管理,访问控制和活动审计等。

官方地址： https://goharbor.io/
github: https://github.com/goharbor/harbor

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible ` 2.6.13`
os `Centos 7.4 X64`

## 角色变量
	software_files_path: "/opt/software"


	harbor_file: "harbor-offline-installer-v1.7.4.tgz"
	harbor_file_path: "{{ software_files_path }}/{{ harbor_file }}"
	harbor_file_url: "https://storage.googleapis.com/harbor-releases/release-1.7.0/{{ harbor_file }}"


	harbor_home: "/harbor_data"
	harbor_hostname: "reg.mydomain.com"
	harbor_ui_url_protocol: https

	harbor_max_job_workers: 10
	harbor_ssl_home: "{{ harbor_home}}/cert"
	harbor_ssl_cert: "{{ harbor_ssl_home }}/server.crt"
	harbor_ssl_cert_key: "{{ harbor_ssl_home }}/server.key"
	harbor_secretkey_path: "{{ harbor_home }}"

	harbor_https_proxy: https://docker.mirrors.ustc.edu.cn/

	harbor_email_server: smtp.mydomain.com
	harbor_email_server_port: 25
	harbor_email_username: sample_admin@mydomain.com
	harbor_email_password: abc
	harbor_email_from: admin <sample_admin@mydomain.com>
	harbor_email_ssl: false
	harbor_email_insecure: false

	harbor_admin_password: Harbor12345

	harbor_openssl: "openssl req -sha256 -x509 -days 3650 -nodes -newkey rsa:4096  -subj '/C=CN/ST=ShangHai/L=ShangHai/O=harbor/OU=harbor/CN={{ harbor_hostname }}' -keyout {{ harbor_ssl_cert_key }} -out {{ harbor_ssl_cert }}"

	harbor_client: false
	harbor_client_user: ""
	harbor_client_pass: ""

## 依赖

docker
docker-compose

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/harbor

## Example Playbook

    安装harbor：
	- hosts: 192.168.77.133
	  vars:
	   - harbor_home: "/harbor_data"
	   - harbor_hostname: "192.168.77.133"
	   - harbor_ui_url_protocol: https
	   - harbor_email_server: smtp.exmail.com
	   - harbor_email_server_port: 465
	   - harbor_email_username: harbor@mydomain.com
	   - harbor_email_password: abc
	   - harbor_email_from: harbor <harbor@mydomain.com>
	   - harbor_email_ssl: true
	  roles:
	   - harbor

    配置harbor客户端:
	- hosts: 192.168.77.133
	  vars:
	   - harbor_client: true
	   - harbor_client_user: admin
	   - harbor_client_pass: Harbor12345
	   - harbor_hostname: "192.168.77.133"
	  roles:
	   - harbor
