# Ansible Role: Keepalived

安装Keepalived

## 介绍
Keepalived是一个用C编写的路由软件。该项目的主要目标是为Linux系统和基于Linux的基础架构提供简单而强大的负载平衡和高可用性设施。负载平衡框架依赖于众所周知且广泛使用的Linux虚拟服务器（IPVS）内核模块，提供Layer4负载均衡。 Keepalived实现了一组检查程序，以根据其健康状况动态地和自适应地维护和管理负载平衡的服务器池。另一方面，VRRP协议实现了高可用性。 VRRP是路由器故障转移的基础。此外，Keepalived为VRRP有限状态机实现了一组挂钩，提供低级和高速协议交互。为了提供最快的网络故障检测，Keepalived实现了BFD协议。 VRRP状态转换可以考虑BFD提示来驱动快速状态转换。 Keepalived框架可以单独使用，也可以一起使用，以提供灵活的基础架构。

官方网站：<https://www.keepalived.org/>
官方文档地址：<https://www.keepalived.org/manpage.html>

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.7.10`
os `Centos 7.4 X64`

## 角色变量
    keepalived_conf: "/etc/keepalived/keepalived.conf"
    
    keepalived_vrrp_instance:
      - name: V1_1
        state: "MASTER"
        interface: "eth0"
        virtual_router_id: "26"
        priority: "100"
        auth_pass: "261232"
        keepalived_vip: "192.168.77.140"
        extra: |
          ! vrrp_instance extra conf
        
    keepalived_virtual_server:
    #  - virtual_server: "192.168.200.100 80"
    #    delay_loop: 6
    #    lb_algo: wrr
    #    lb_kind: NAT
    #    persistence_timeout: 50
    #    protocol: TCP
    #    real_server:
    #    - server: "192.168.201.100 80"
    #      weight: 1
    #      tcp_check:
    #        connect_timeout: 10  
    #        nb_get_retry: 3
    #        delay_before_retry: 3
    #        connect_port: 80
    #      extra: |
    #        ! real_server extra conf
    #    extra: |
    #     ! virtual_server extra conf
    
    keepalived_conf_extra: ""

## 依赖

epel

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/keepalived

## Example Playbook
    单主
    - hosts: node1
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "MASTER"
          vip: "192.168.77.140"
      roles:
      - { role: keepalived }
    
    - hosts: node2
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "BACKUP"
          vip: "192.168.77.140"
      roles:
      - { role: keepalived}
    
    单主单播
    - hosts: node1
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "MASTER"
          vip: "192.168.77.140"
          unicast_peer: "192.168.77.131"
      roles:
      - { role: keepalived }
    
    - hosts: node2
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "BACKUP"
          vip: "192.168.77.140"
          unicast_peer: "192.168.77.130"
      roles:
      - { role: keepalived}
    
    单主lvs
    - hosts: node1
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "MASTER"
          vip: "192.168.77.140"
      - keepalived_virtual_server:
        - virtual_server: "192.168.77.140 80"
          delay_loop: 6
          lb_algo: wrr
          lb_kind: DR
          persistence_timeout: 50
          real_server:
          - server: "192.168.77.132 80"
            weight: 1
            tcp_check:
              connect_timeout: 10 
              nb_get_retry: 3
              delay_before_retry: 3
              connect_port: 80
          - server: "192.168.77.133 80"
            weight: 1
            tcp_check:
              connect_timeout: 10 
              nb_get_retry: 3
              delay_before_retry: 3
              connect_port: 80
    
      roles:
      - { role: keepalived }
    
    - hosts: node2
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "BACKUP"
          vip: "192.168.77.140"
      - keepalived_virtual_server:
        - virtual_server: "192.168.77.140 80"
          delay_loop: 6 
          lb_algo: wrr
          lb_kind: DR
          persistence_timeout: 50
          real_server:
          - server: "192.168.77.132 80"
            weight: 1 
            tcp_check:
              connect_timeout: 10    
              nb_get_retry: 3 
              delay_before_retry: 3 
              connect_port: 80
          - server: "192.168.77.133 80"
            weight: 1
            tcp_check:
              connect_timeout: 10
              nb_get_retry: 3
              delay_before_retry: 3
              connect_port: 80
      roles:
      - { role: keepalived}
    
    双主
    - hosts: node1
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "MASTER"
          vip: "192.168.77.140"
        - name: V1_2
          state: "BACKUP"
          virtual_router_id: "141"
          auth_pass: "v2hello"
          vip: "192.168.77.141"
      roles:
      - { role: keepalived }
    
    - hosts: node2
      vars:
      - keepalived_vrrp_instance:
        - name: V1_1
          state: "BACKUP"
          vip: "192.168.77.140"
        - name: V1_2
          state: "MASTER"
          auth_pass: "v2hello"
          virtual_router_id: "141"
          vip: "192.168.77.141"
      roles:
      - { role: keepalived}

## 使用
```
systemctl start keepalived
systemctl stop keepalived
systemctl restart keepalived
systemctl status keepalived
```

