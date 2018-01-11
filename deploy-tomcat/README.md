# Ansible Role: deploy-tomcat

部署war包至tomcat容器

## 要求

- 此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    # 发布的代码文件，包含绝对路径，如:/tmp/test.war
    deploy_file: ""

    # tomcat服务的端口
    deploy_port: "8080"

    # tomcat服务用户
    deploy_service_user: "tomcat"

    # tomcat服务的名称
    deploy_service_name: "tomcat{% if deploy_port != 8080 %}{{ deploy_port }}{% endif %}"

    # 发布服务的家目录
    deploy_file_workpath: "/usr/local/{{ deploy_service_name }}/webapps/ROOT"

    # 启动脚本
    deploy_service_start_script: "/etc/init.d/{{ deploy_service_name }}"

    # 临时目录
    deploy_file_path: "/tmp/{{ deploy_service_name }}-ansible-snap"

    # 上线代码的存储目录
    deploy_new_path: "{{ deploy_file_path }}/new"

    # 当前代码(也就是上一版本的代码)的存储目录
    deploy_pre_path: "{{ deploy_file_path }}/pre"

    # 历史代码存储目录
    deploy_old_path: "{{ deploy_file_path }}/old"

    # 是否回滚
    deploy_rollback: false

## 依赖
tomcat

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/deploy-tomcat

## Example Playbook

    # 发布代码
    - hosts: node1
      roles:
        - role: { role: deploy-tomcat, deploy_port: 8071, deploy_file：/root/tomcat_*_test.war }
      
    # 回滚代码
    - hosts: node1
      roles:
        - role: { role: deploy-tomcat, deploy_rollback: true }