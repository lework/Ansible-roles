# Ansible Role: airflow

安装airflow

## 介绍

Airflow 被 Airbnb 内部用来创建、监控和调整数据管道。任何工作流都可以在这个使用 Python 编写的平台上运行（目前加入 Apache 基金会孵化器）。

Airflow 允许工作流开发人员轻松创建、维护和周期性地调度运行工作流（即有向无环图或成为DAGs）的工具。在Airbnb中，这些工作流包括了如数据存储、增长分析、Email发送、A/B测试等等这些跨越多部门的用例。这个平台拥有和 Hive、Presto、MySQL、HDFS、Postgres和S3交互的能力，并且提供了钩子使得系统拥有很好地扩展性。除了一个命令行界面，该工具还提供了一个    基于Web的用户界面让您可以可视化管道的依赖关系、监控进度、触发任务等。  

github地址：https://github.com/apache/incubator-airflow
官方文档地址：https://airflow.incubator.apache.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
	airflow_home: "/airflow"
	airflow_tmpdir: "/tmp/airflow"
	airflow_bin: "/usr/local/bin/airflow"
	airflow_user: "airflow"
	airflow_extra: [hive,hdfs,jdbc,mysql,async,postgres,rabbitmq,qds,password,ldap]
	airflow_db: "airflow"
	mysql_host: ""
	mysql_port: ""
	mysql_user: ""
	mysql_password: ""
	create_db: true
	change_utctime: true
	airflow_port: 8080

	env: "HOME=/home/{{ airflow_user }},AIRFLOW_HOME={{ airflow_home }},TMPDIR={{ airflow_tmpdir }}"
	

## 依赖
python2.7
supervisor

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/airflow

## Example Playbook

    - hosts: node1
      vars:
        airflow_home: '/airflow'
        mysql_host: 192.168.77.128
        mysql_port: 3306
        mysql_user: root
        mysql_password: 123456
        supervisor_name: airflow
        airflow_port: 8081
        supervisor_program: 
          - { name: 'webserver', command: '/usr/local/bin/airflow webserver', user: 'airflow' }
          - { name: 'scheduler', command: '/usr/local/bin/airflow scheduler', user: 'airflow' }
      roles:
        - { role: python2.7 }
        - { role: airflow }
        - { role: supervisor }
