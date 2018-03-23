# Ansible Role: kerberos client

安装kerberos client服务

## 介绍
Kerberos：网络认证协议
（Kerberos: Network Authentication Protocol）

Kerberos 是一种网络认证协议，其设计目标是通过密钥系统为客户机/ 服务器应用程序提供强大的认证服务。该认证过程的实现不依赖于主机操作系统的认证，无需基于主机地址的信任，不要求网络上所有主机的物理安全，并假定网络上传送的数据包可以被任意地读取、修改和插入数据。在以上情况下， Kerberos 作为一种可信任的第三方认证服务，是通过传统的密码技术（如：共享密钥）执行认证服务的。

- 官方地址：http://web.mit.edu/kerberos/
- 官方文档地址：http://web.mit.edu/~kerberos/krb5-devel/doc/index.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

- ansible `2.3.0.0`
- os `Centos 6.7 X64`
- python `2.6.6`

## 角色变量
    kerberos_realm_name: EXAMPLE.COM                           # Kerberos realms
    kerberos_kdc_hostname: kerberos                               # kerberos server 主机名
    kerberos_kdc_ipaddress: 127.0.0.1                           # kerberos server 主机地址
    kerberos_admin_hostname: "{{ kerberos_kdc_hostname }}"     # kerneros administration server 主机名
    kerberos_admin_hostname: "{{ kerberos_kdc_ipaddress }}"    # kerneros administration server 主机地址
    kerberos_dns_lookup_realm: "false"                         # 是否通过dns查询realm
    kerberos_dns_lookup_kdc: "false"                           # 是否通过dns查询kdc
    kerberos_ticket_lifetime: "24h"                            # 凭证生效的时限
    kerberos_renew_lifetime: "7d"                              # 凭证最长可以被延期的时限
    kerberos_forwardable: "true"                               # 获取凭证

## 依赖
None

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/kerberos-client

## Example Playbook

    - hosts: node2
      vars:
        kerberos_realm_name: "KERBEROSTEST.COM"
        kerberos_kdc_hostname: "node1"
        kerberos_kdc_ipaddress: "192.168.77.129"
      roles:
        - kerberos-client

        
## 使用

登录kdc admin Server
`kadmin`

在管理员状态下使用增删改查

`addprinc`  增加用户
`delprinc`  删除用户
`modprinc`  修改用户
`listprincs`  查看用户

生成keytab
`kadmin:xst -k /xxx/xxx/kerberos.keytab hdfs/hadoop`

查看当前的认证用户
`klist`

认证用户
`kinit -kt /xx/xx/kerberos.keytab hdfs/hadoop1`

删除当前的认证缓存
`kdestory`

更新ticket
`kinit -R`

修改renewlife
`modprinc -maxrenewlife 1week krbtgt/HADOOP.COM@HADOOP.COM`