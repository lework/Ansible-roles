# Ansible Role:docker-swarm

安装docker-swarm集群

## 介绍

swarm是Docker公司在2014年12月初发布的一套较为简单的工具，用来管理Docker集群，它将一群Docker宿主机变成一个单一的虚拟的主机。



## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    swarm_advertise_addr: "{{ ansible_default_ipv4.address }}"
    swarm_node: 'master'
    # (master, node)
    swarm_master: ""
    # ip address

## 依赖

centos 7.3 以上版本

docker

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/docker-swarm

## Example Playbook
    部署集群
    - hosts: node4
      roles:
        - docker
        - docker-swarm

    - hosts: node5
      roles:
        - docker
        - {role: docker-swarm, swarm_node: 'node', swarm_master: '192.168.77.133'}


## 使用
```
docker node ls
```