# Ansible Role: Tomcat

安装tomcat应用

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

os `Centos 7.2 X64`

python `2.7.5`

## 角色变量
    
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    java_home: "{{ ansible_env.JAVA_HOME | default('/usr/java/jdk1.7.0_80') }}"

    tomcat_version: "7.0.85"
    tomcat_file: "apache-tomcat-{{ tomcat_version }}.tar.gz"
    tomcat_path: "{{ software_install_path }}/apache-tomcat-{{ tomcat_version }}"
    tomcat_file_path: "{{ software_files_path }}/{{ tomcat_file }}"
    tomcat_file_url: "http://archive.apache.org/dist/tomcat/tomcat-7/v{{ tomcat_version }}/bin/apache-tomcat-{{ tomcat_version }}.tar.gz"

    tomcat_enabled: true
    tomcat_server_active: false
    tomcat_ajp_active: false
    tomcat_hostname: localhost
    tomcat_user: tomcat
    tomcat_server_port: 8005
    tomcat_catalina_port: 8080
    tomcat_catalina_ajp_port: 8009
    tomcat_catalina_redirect_port: 8443
    tomcat_unpackWARs: true
    tomcat_autoDeploy: true

    tomcat_services_name: "tomcat{% if tomcat_catalina_port != 8080 %}{{ tomcat_catalina_port }}{% endif %}"

    tomcat_work_path: "{{ software_install_path }}/{{ tomcat_services_name }}"
    tomcat_daemon_native_path: "{{ tomcat_work_path }}/bin/commons-daemon-1.1.0-native-src"
    tomcat_catalina_opts: "-server -Xms1024m -Xmx1024m -XX:PermSize=256M -XX:MaxNewSize=256m -XX:MaxPermSize=256m -Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Djava.awt.headless=true"

    
## 依赖

java

## github地址

https://github.com/kuailemy123/Ansible-roles/tree/master/tomcat

## Example Playbook
    安装tomcat7
    - hosts: node1
      roles:
       - tomcat

    - hosts: node1
      roles:
       - { role: tomcat, tomcat_catalina_port: 8081, tomcat_server_port: 8005}
       - { role: tomcat, tomcat_catalina_port: 8082, tomcat_server_port: 8006}
       
    安装tomcat8
    - hosts: node1
      vars:
       - java_version: "1.8"
       - tomcat_version: "8.5.28"
      roles:
       - java
       - tomcat

## 使用

`centos 6`
```
service tomcat
Usage: tomcat ( commands ... )
commands:
  run               Start Tomcat without detaching from console
  start             Start Tomcat
  stop              Stop Tomcat
  version           What version of commons daemon and Tomcat
                    are you running?
```
`centos 7` 
```
systemctl start tomcat
systemctl status tomcat
systemctl stop tomcat
```
