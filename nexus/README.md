# Ansible Role: nexus

安装nexus

## 介绍
Sonatype Nexus是世界领先的仓库管理系统，在世界范围内Nexus OSS，Nexus Pro或Nexus Pro CLM将近50000次安装。

官方网站：https://www.sonatype.com/
官方文档地址：http://books.sonatype.com/nexus-book/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: `2.3.1.0`
    os: `Centos 7.2 X64`
    python: `2.7.5`

ansible管理主机

    os: `Centos 6.7 X64, Centos 7.2 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    nexus_version: "3.4.0-02"

    nexus_file: "nexus-{{ nexus_version }}-unix.tar.gz"
    nexus_file_path: "{{ software_files_path }}/{{ nexus_file }}"
    nexus_file_url: "https://sonatype-download.global.ssl.fastly.net/nexus/3/{{ nexus_file }"

    nexus_user: 'nexus'
    nexus_group: 'nexus'

    nexus_port: 8081
    nexus_workspace: "{{ software_install_path }}/nexus"

    java_home: "{{ ansible_env.JAVA_HOME | default('/usr/java/jdk1.8.0_144') }}"
    
## 依赖

jdk 1.8

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/nexus

## Example Playbook
    #默认安装nexus
    - hosts: node1
      vars:
        - java_version: "1.8"
      
      roles:
        - java
        - nexus
      
    # 指定端口
    - hosts: node1
      vars:
        - java_version: "1.8"
        - nexus_port: 28081
      
      roles:
        - java
        - nexus
      
## 使用

```
# centos6
/etc/init.d/nexus 
Usage: /etc/init.d/nexus {start|stop|reload|configtest|status|force-reload|upgrade|restart|reopen_logs}

# centos7
systemctl status nexus
systemctl start nexus
systemctl stop nexus

# web login
admin/admin123
```