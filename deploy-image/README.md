# Ansible Role: deploy-image

部署docker image

## 要求

- 此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.3`

os `Centos 7.4.1708 X64`

docker `18.03.1-ce`


## 角色变量

    # 代码文件
    deploy_service_file: ""

    # 代码路径
    deploy_service_path: ""

    # 应用的端口
    deploy_service_port: ""

    # 等待多少秒检测端口
    deploy_service_port_delay: 1

    # 检测端口超时时间
    deploy_service_port_timeout: 90

    # image的名称
    deploy_image_name: ""

    # image的tag
    deploy_image_tag: "{{ deploy_image_name }}:latest"

    # image的Dockerfile
    deploy_image_dockerfile: ""

    # 网络
    deploy_container_network: "default"

    # container的名称
    deploy_container_name: "{{ deploy_image_name }}"

    # container的主机名
    deploy_container_hostname: "{{ deploy_image_name }}"

    # container端口绑定
    deploy_container_publish: 
      - "{{ deploy_service_port}}:{{ deploy_service_port}}"

    # container目录绑定
    deploy_container_volume:
      - "/tmp/:/tmp/"
      
    # container 环境变量
    deploy_container_env: []
    
    # container ip
    deploy_container_ip: ""  

    deploy_docker_bin: "/usr/bin/docker"
    # image编译脚本
    deploy_image_build: >
      {{ deploy_docker_bin }} build --no-cache 
      --build-arg APP_FILE={{ deploy_service_file }} 
      --build-arg SERVER_PORT={{ deploy_service_port }} 
      -f {{ deploy_image_dockerfile}} 
      -t {{ deploy_image_tag }}
      {{ deploy_service_path }}
      
    # image上传脚本
    deploy_image_push: >
      {{ deploy_docker_bin }} push {{ deploy_image_tag }}

    # image拉取脚本
    deploy_image_pull: >
      {{ deploy_docker_bin }} pull {{ deploy_image_tag }}
      
    # container关闭命令
    deploy_container_stop: >
      {{ deploy_docker_bin }} stop {{ deploy_container_name }} &&
      {{ deploy_docker_bin }} rm {{ deploy_container_name }} ||
      echo error

    # container运行命令
    deploy_container_run: >
      {{ deploy_docker_bin }} run -tid
      --net {{ deploy_container_network }}
      --name {{ deploy_container_name }}
      -h {{ deploy_container_hostname }}
      {% for p in deploy_container_publish %}-p {{ p }} {% endfor %}
      {% for v in deploy_container_volume %}-v {{ v }} {% endfor %}
      {% if deploy_container_ip %}--ip {{ deploy_container_ip }}{% endif %} 
      --restart=always
      {{ deploy_image_tag }}

    # 清除无用的镜像
    deploy_clear: true
    deploy_clear_run: >
      {{ deploy_docker_bin }} rmi --force $({{ deploy_docker_bin }} images | grep 'none' | awk '{print $3}')

    # 验证uri
    deploy_verify_uri: ""
    deploy_verify_url: "http://127.0.0.1:{{ deploy_service_port }}{{ deploy_verify_uri }}"

    # 是否回滚
    deploy_rollback: false



## 依赖

- docker
- docker hub

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/deploy-image

## Example Playbook

    # 发布image
    - hosts: docker3
      serial: "50%"
      gather_facts: false
      vars:
       - deploy_service_file: "test.war"
       - deploy_service_path: "/data/jenkins/workspace/test/dist/"
       - deploy_service_port: 26381
       - deploy_image_name: "test"
       - deploy_image_tag: "127.0.0.1/docker3/test:master"
       - deploy_image_dockerfile: "/opt/images/Dockerfile_tomcat7"
       - deploy_container_network: "test"
       - deploy_container_publish:
         - "26381:26381"
       - deploy_container_volume:
         - "/tmp/:/tmp/"
         - "/var/log/test:/usr/local/tomcat/logs"
      roles:
        - deploy-image

    # 回滚image
    - hosts: docker3
      serial: "50%"
      gather_facts: false
      vars:
       - deploy_rollback: true
       - deploy_service_port: 26381
       - deploy_image_name: "test"
       - deploy_image_tag: "127.0.0.1/docker3/test:v1.0"
       - deploy_container_network: "test"
       - deploy_container_publish:
         - "26381:26381"
       - deploy_container_volume:
         - "/tmp:/tmp"
         - "/var/log/test:/usr/local/tomcat/logs"
      roles:
        - deploy-image
