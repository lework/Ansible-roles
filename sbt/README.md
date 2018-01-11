# Ansible Role: sbt

添加Scala编译环境

## 说明
SBT = (not so) Simple Build Tool,是scala的构建工具。

官方网站：http://www.scala-sbt.org/
官方文档：http://www.scala-sbt.org/0.13/docs/zh-cn/index.html
github: https://github.com/sbt/sbt

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    sbt_version: "0.13.15"
    sbt_file: "sbt-{{ sbt_version }}.tgz"
    sbt_file_path: "{{ software_files_path }}/{{ sbt_file }}"
    sbt_install_path: "{{ software_install_path }}/apache-maven-{{ mvn_version }}"
    sbt_file_url: "https://downloads.lightbend.com/sbt/{{ sbt_version }}/{{ sbt_file }}"

    sbt_maven: "http://maven.aliyun.com/nexus/content/groups/public/"
    sbt_typesafe: "http://dl.bintray.com/typesafe/ivy-releases/"
    sbt_ivy_plugin: "http://dl.bintray.com/sbt/sbt-plugin-releases/"


## 依赖

Java 1.6+

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/sbt

## Example Playbook

    - hosts: node1
      roles:
        - sbt
    
    - hosts: node1
      roles:
        - { role: sbt, sbt_version: '0.13.15' }
