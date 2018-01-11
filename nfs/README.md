# Ansible Role: nfs

配置nfs服务端

## 介绍
NFS（Network File System）即网络文件系统，是FreeBSD支持的文件系统中的一种，它允许网络中的计算机之间通过TCP/IP网络共享资源。在NFS的应用中，本地NFS的客户端应用可以透明地读写位于远端NFS服务器上的文件，就像访问本地文件一样。

- RFC 1094:  http://www.faqs.org/rfcs/rfc1094.html
- Linux NFS-HOWTO: http://www.tldp.org/HOWTO/NFS-HOWTO/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量
    nfs_exports: 
        - /nfs_data *(rw,all_squash,async)

## 依赖
rpcbind

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/nfs

## Example Playbook

    - hosts: node1
      vars:
        - nfs_exports: 
           - /nfs_data *(rw,all_squash,async)
           - /nfs_data2 *(rw,all_squash,async)
           - /nfs_data3 *(rw,all_squash,async)
      roles:
        - role: nfs

## 端口

- rpcbind 111
- mountd 892
- rquotad 875
- nfs 2049
- lockd udp 32769
- lockd tcp 32803

## 使用

```
~]# /etc/init.d/rpcbind 
Usage: /etc/init.d/rpcbind {start|stop|status|restart|reload|force-reload|condrestart|try-restart}
~]# /etc/init.d/nfs
Usage: nfs {start|stop|status|restart|reload|force-reload|condrestart|try-restart|condstop}

```
