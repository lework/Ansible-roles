# Ansible Role: vsftp

配置ftp服务端

## 介绍
vsftpd 是“very secure FTP daemon”的缩写，安全性是它的一个最大的特点。vsftpd 是一个 UNIX 类操作系统上运行的服务器的名字，它可以运行在诸如 Linux、BSD、Solaris、 HP-UNIX等系统上面，是一个完全免费的、开放源代码的ftp服务器软件，支持很多其他的 FTP 服务器所不支持的特征。

- 官方： http://vsftpd.beasts.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`  `Centos 7.2 X64`
python `2.6.6`

## 角色变量
    vsftpd_packages:
      - vsftpd
      - libsemanage-python
      - libselinux-python
      - pam
      - db4-utils
      
    vsftpd_listen_port: 21
    vsftpd_data_port: 20
    vsftpd_pasv_min_port: 30000
    vsftpd_pasv_max_port: 31000

    vsftpd_local_umask: '022'
    vsftpd_share_path: '/ftp_share'
    vsftpd_banner: "Welcome to Ftp Server!"
    vsftpd_syslog_enable: false

    vsftpd_log_file: '/var/log/vsftpd.log'
    vsftpd_xferlog_file: '/var/log/xferlog'

    vsftpd_options: ""
    # vsftpd_options: |
    #   max_per_ip: 5
    #   max_clients: 100
    vsftpd_anon: true
    vsftpd_local_users: []
    # vsftpd_users:
    #  - name: alice
    #    password: "ecila"
    #    home: /ftp_alice

    vsftpd_vusers: []
    # vsftpd_vusers:
    #  - name: alice
    #    password: ecila
    #    local_root: '/alice_share'
    #    conf: |
    #      local_umask=011

    vsftpd_userfile: "/etc/vsftpd/vuser"
    vsftpd_userdb: "/etc/vsftpd/vuser.db"
    vsftpd_userconf: "/etc/vsftpd/vuser_conf"


## 依赖
None

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/vsftpd

## Example Playbook
    # 默认配置，匿名登录
    - hosts: node1
      roles:
        - role: vsftpd
    
    # 本地用户登录
    - hosts: node1
      vars:
        - vsftpd_local_users:
        - name: alice
          password: "123"
          home: /ftp_alice
        - name: lili
          password: "123"
      roles:
        - vsftpd
       
    # 虚拟用户登录
    - hosts: node1
      vars:
        - vsftpd_share_path: '/ftp_vuser_share'
        - vsftpd_vusers: 
        - name: test1
          password: 123
        - name: test2
          password: 123
          local_root: '/ftp_test2_home'
          conf: |
            local_root=/ftp_test2_home
            local_umask=011
      roles: 
          - vsftpd
## 端口

- 21
- 20

## 使用

```
~]# service vsftpd
Usage: /etc/init.d/vsftpd {start|stop|restart|try-restart|force-reload|status}
```
