# Ansible Role: samba

配置Samba服务端

## 介绍
Samba是在Linux和UNIX系统上实现SMB协议的一个免费软件，由服务器及客户端程序构成。SMB（Server Messages Block，信息服务块）是一种在局域网上共享文件和打印机的一种通信协议，它为局域网内的不同计算机之间提供文件及打印机等资源的共享服务。SMB协议是客户机/服务器型协议，客户机通过该协议可以访问服务器上的共享文件系统、打印机及其他资源。通过设置“NetBIOS over TCP/IP”使得Samba不但能与局域网络主机分享资源，还能与全世界的电脑分享资源。

- 官方： https://www.samba.org
- 配置文件： https://www.samba.org/samba/docs/man/manpages-3/smb.conf.5.html
- 文档:  https://www.samba.org/samba/docs/Samba-Guide.pdf
- HOWTO: https://www.samba.org/samba/docs/Samba-HOWTO-Collection.pdf

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    samba_packages:
      - samba-common
      - samba
      - samba-client
      - cifs-utils
      - libselinux-python
      
    samba_services:
      - smb
      - nmb
      
    samba_workgroup: 'WORKGROUP'
    samba_server_string: 'Fileserver %m'
    samba_netbios_name: "{{ ansible_hostname | d() }}"
    samba_log_size: 50000
    samba_log_file: '/var/log/samba/log'
    samba_interfaces: []
    samba_security: 'user'
    samba_passdb_backend: 'tdbsam'
    samba_map_to_guest: 'bad user'
    samba_guest_account: 'nobody'
    samba_load_printers: false
    samba_load_homes: false
    samba_full_audit: true
    samba_shares_path: '/samba_shares'
    samba_users: []
    # samba_users:
    #  - name: alice
    #    password: ecila
    samba_shares: 
      - name: default
        comment: 'default share'
        guest_ok: yes
        directory_mode: 777
        recycle: true


## 依赖
None

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/samba

## Example Playbook
    # 默认配置，匿名访问/samba_shares目录
    - hosts: node1
      roles:
      - role: samba
    
    # 定义访问用户和共享目录
    - hosts: node1
      vars:
       - samba_users:
          - name: alice
            password: 123
       - samba_shares:
          - name: customize_share
            comment: 'customize share'
            path: /customize_share
            valid_users: alice
            owner: alice
      roles: 
       - samba

## 端口

- 139
- 445

## 使用

```
~]# /etc/init.d/smb 
Usage: /etc/init.d/smb {start|stop|restart|reload|configtest|status|condrestart}
~]# /etc/init.d/nmb 
Usage：/etc/init.d/nmb {start|stop|restart|reload|status|condrestart}
```
