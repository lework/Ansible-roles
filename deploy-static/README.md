# Ansible Role: deploy-static

部署静态文件,如web页面、php应用

## 要求

- 此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.1`
os `Centos 7.2.1511 X64`

## 角色变量
    # 发布的代码文件，包含绝对路径，如:/tmp/test.jar
    deploy_file: ""

    # 发布服务名称
    deploy_service: ""

    # 发布文件的用户
    deploy_service_user: ""

    # 发布服务的家目录
    deploy_service_workpath: "/Microservices/{{ deploy_service }}"

    # 临时目录
    deploy_file_path: "/packages"

    # 上线代码的存储目录
    deploy_code_online_path: "{{ deploy_file_path }}/online/{{ deploy_service }}"

    # 当前代码(也就是上一版本的代码)的存储目录
    deploy_code_previous_path: "{{ deploy_file_path }}/previous/{{ deploy_service }}"

    # 历史代码存储目录
    deploy_code_history_path: "{{ deploy_file_path }}/history/{{ deploy_service }}"

    # 是否回滚
    deploy_rollback: false

    # 检查uri
    deploy_verify_uri: ""


## 依赖


## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/deploy-static

## Example Playbook

    # 发布代码
        - hosts: node1
          vars:
            - deploy_file: /tmp/web.tar.gz
            - deploy_service: web
            - deploy_service_user: apache
            - deploy_verify_uri: "/index.html"
          roles:
            - deploy-static
      
    # 回滚代码，只能回滚上一次线上代码，应用于当前发布程序有问题回滚正常版本场景。
        - hosts: node1
          vars:
            - deploy_rollback: true
            - deploy_service: web
            - deploy_service_user: apache
            - deploy_verify_uri: "/index.html"
          roles:
            - deploy-static
