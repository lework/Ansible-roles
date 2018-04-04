# Ansible Role:shipyard

安装shipyard

## 介绍

简化对横跨多个主机的Docker容器集群进行管理, 目前作者已不再维护

github: https://github.com/shipyard/shipyard

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    shipyard_lang: 'cn'
    # (cn, en)
    shipyard_action: 'deploy'
    # (deploy, upgrade, node, remove)

    shipyard_port: 8080
    shipyard_proxy_port: 2375
    shipyard_discover: ''
    # etcd://node:4001

## 依赖

centos 7.3 以上版本

docker

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/shipyard

## Example Playbook
    部署单节点
    - hosts: node4
      roles:
        - docker
        - shipyard

    部署多节点
    - hosts: node4
      roles:
        - docker
        - shipyard

    - hosts: node5
      roles:
        - docker
        - {role: shipyard, shipyard_action: 'node', shipyard_discover: 'etcd://192.168.77.133:4001'}


## 使用
```
docker ps -a
```
