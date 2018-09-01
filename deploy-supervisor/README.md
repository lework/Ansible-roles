# Ansible Role: deploy-supervisor

部署spring boot 应用, spring boot由supervisor管理

## 要求

- 此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.1`
os `Centos 7.2.1511 X64`
python `2.7.5`
supervisor `3.3.4`

## 角色变量
	# 发布的代码文件，包含绝对路径，如:/tmp/test.jar
    deploy_file: ""

    # supervisor应用的端口
    deploy_service_port: ""

    # 等待多少秒检测端口
    deploy_service_port_delay: 1

    # 检测端口超时时间
    deploy_service_port_timeout: 90

    # supervisor应用的名称
    deploy_service_name: ""

    # 服务文件
    deploy_service_file: ""

    # 发布服务用户
    deploy_service_user: "spring"

    # 发布服务的家目录
    deploy_service_workpath: "/Microservices"

    # supervisorctl 管理程序
    deploy_service_start_script: "/usr/bin/supervisorctl"

    # 验证uri
    deploy_verify_uri: ""
    deploy_verify_url: "http://127.0.0.1:{{ deploy_service_port }}{{ deploy_verify_uri }}"

    # 临时目录
    deploy_file_path: "/packages"

    # 上线代码的存储目录
    deploy_code_online_path: "{{ deploy_file_path }}/online"

    # 当前代码(也就是上一版本的代码)的存储目录
    deploy_code_previous_path: "{{ deploy_file_path }}/previous"

    # 历史代码存储目录
    deploy_code_history_path: "{{ deploy_file_path }}/history"

    # 是否回滚
    deploy_rollback: false


## 依赖
- supervisor
- {{ deploy_service_name }}的值 应为supervisor应用名称

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/deploy-supervisor

## Example Playbook

    # 发布代码
        - hosts: node1
          vars:
            - deploy_file: /opt/test.jar
            - deploy_service_name: test_spingboot
            - deploy_service_port: 8084
            - deploy_verify_uri: "/"
          roles:
            - deploy-supervisor
      
    # 回滚代码，只能回滚上一次线上代码，应用于当前发布程序有问题回滚正常版本场景。
        - hosts: node1
          vars:
            - deploy_rollback: true
            - deploy_service_file: test.jar
            - deploy_service_name: test_spingboot
            - deploy_service_port: 8084
            - deploy_verify_uri: "/"
          roles:
            - deploy-supervisor
