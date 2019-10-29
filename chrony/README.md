# Ansible Role: chrony

安装chrony,实现时间同步.

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.8.5`
os `Centos 7.4 X64`

## 角色变量


## 依赖

没有

## github地址
https://github.com/lework/Ansible-roles/tree/master/chrony

## Example Playbook

    - hosts: servers
      roles:
      - chrony

	  
## 验证
```
chronyc sourcestats
210 Number of sources = 6
Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
119.28.206.193              4   4     6    -45.185   2425.458  -9572us   309us
de-user.deepinid.deepin.>   4   3     8   +530.643  32458.904  -1419us  4953us
ntp-b2.nict.go.jp           4   3     7   -216.268  20531.617    +24ms  2677us
149.28.28.160.vultr.com     4   3     7    +11.863  22120.141    +24ms  2745us
ntp.wdc1.us.leaseweb.net    0   0     0     +0.000   2000.000     +0ns  4000ms
sv1.ggsrv.de                0   0     0     +0.000   2000.000     +0ns  4000m

chronyc sources -v
chronyc tracking 
```