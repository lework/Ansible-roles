# Ansible Role: rsync

安装rsync服务

## 介绍
rsync是类unix系统下的数据镜像备份工具——remote sync。一款快速增量备份工具 Remote Sync，远程同步 支持本地复制，或者与其他SSH、rsync主机同步。

官方地址： http://rsync.samba.org/
官方文档地址：http://rsync.samba.org/documentation.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    rsync_user: "rsync"
    rsync_logdir: "/var/log/rsyncd"
    rsync_conf: "/etc/rsyncd.conf"

    rsync_authusers: [] # ["test:123456"]
    rsync_passfile: "/etc/rsyncd.password"

    rsync_port: 873
    rsync_maxconn: 200
    rsync_timeout: 300
    rsync_chroot: no
    rsync_shares: {}

## 依赖


## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/rsync

## Example Playbook

    - hosts: node1
      roles:
      - role: rsync
        rsync_authusers: ["t1:123456","t2:1234567"]
        rsync_shares:
            - name: data1
              comment: Public data1
              path: /data/1
              authuser: t1
              passfile: /etc/rsyncd.password
              readonly: false
              list: false
              excludes: ["test.txt","*.h"]
            - name: data2
              comment: Public data2
              path: /data/2

## 使用
启动 rsync --daemon --config=/etc/rsyncd.conf