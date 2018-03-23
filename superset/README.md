# Ansible Role: superset

安装superset

## 介绍
Superset（Caravel）是由Airbnb（知名在线房屋短租公司）开源的数据分析与可视化平台（曾用名Caravel、Panoramix），该工具主要特点是可自助分析、自定义仪表盘、分析结果可视化（导出）、用户/角色权限控制，还集成了一个SQL编辑器，可以进行SQL编辑查询等。

Superset（Caravel）核心功能：

1.快速创建数据可视化互动仪表盘
2.丰富的可视化图表模板，灵活可扩展
3.细粒度高可扩展性的安全访问模型，支持主要的认证供应商（数据库、OpenID、LDAP、OAuth 等）
4.简洁的语义层，可以控制数据资源在 UI 的展现方式
5.与 Druid（其实它貌似就是为了druid而生的）深度集成，可以快速解析大规模数据集
6.快速的通过配置装载仪表盘等


github地址： https://github.com/airbnb/superset
官方文档地址：http://airbnb.io/superset/installation.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    superset_bin: "/usr/local/bin/superset"
    superset_user: "superset"
    superset_db: "superset"
    superset_app: "superset"
    superset_username: "admin"
    superset_firstname: "admin"
    superset_lastname: "admin"
    superset_email: "admin@example.com"
    superset_password: "123456"
    mysql_host: ""
    mysql_port: ""
    mysql_user: ""
    mysql_password: ""
    create_db: true
    superset_port: 8080

    env: "HOME=/home/{{ superset_user }}"
    

## 依赖
python2.7
supervisor

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/superset

## Example Playbook

    - hosts: node1
      vars:
        superset_home: '/superset'
        mysql_host: 192.168.77.128
        mysql_port: 3306
        mysql_user: root
        mysql_password: 123456
        supervisor_name: superset
        supervisor_program: 
          - { name: 'superset', command: '/usr/local/bin/superset runserver', user: 'superset' }
      roles:
       - { role: python2.7 }
       - { role: superset }
       - { role: supervisor }
       
       
## 管理

使用supervisor启动superset
/usr/local/bin/supervisord -c /etc/supervisor/conf/superset.conf

启动superset程序
service superset start

关闭superset程序
service superset stop

关闭supervisor
service superset shutdown