# Ansible Role: ntp

安装ntp客户端,实现时间同步.

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.8.1`
os `Centos 7.4 X64`

## 角色变量


## 依赖

没有

## github地址
https://github.com/lework/Ansible-roles/tree/master/ntp

## Example Playbook

    - hosts: servers
      roles:
      - ntp

	  
## 验证
```
ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 ntp7.flashdance 77.40.226.114    2 u   25   64    1  286.685    3.939   0.000
 crimson.en.kku. .PPS.            1 u   24   64    1  123.759  -24.300   0.000
 202-65-114-202. .INIT.          16 u    -   64    0    0.000    0.000   0.000
```