# Ansible Role: docker-compose

安装docker-compose

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`
python `2.7.5`
os `Centos 7.4 X64`
docker `17.12.0-ce`

## 角色变量
    docker_compose_version: "1.19.0"

    docker_compose_url: "https://github.com/docker/compose/releases/download/{{ docker_compose_version }}/docker-compose-Linux-x86_64"

    docker_exec_path: "/usr/local/bin/docker-compose"

## 依赖

docker

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/docker-compose

## Example Playbook

    - hosts: node1
      roles:
        - docker-compose
        
## 使用
```
docker-compose --help
```
