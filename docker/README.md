# Ansible Role: docker

安装docker

## 介绍

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口。

官网: https://www.docker.com/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    docker_repo: "https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo"

    docker_old:
      - docker
      - docker-common
      - docker-selinux
      - docker-engine

    docker_packages:
      - lvm2
      - yum-utils
      - device-mapper-persistent-data
      
    docker_start: true
    docker_registry_mirrors: ["https://docker.mirrors.ustc.edu.cn/", "https://registry.docker-cn.com"]
    docker_insecure_registries: []

## 依赖

centos 7.3 以上版本

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/docker

## Example Playbook

    - hosts: node1
      roles:
        - docker
        
## 使用
```
systemctl start docker
systemctl stop docker
systemctl status docker
```
