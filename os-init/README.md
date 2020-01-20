# Ansible Role: OS INIT

针对 linux 系统进行一些初始化操作。

## 要求

此角色在Debian和RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: 2.9.1
    os: Centos 7.4 X64
    python: 2.7.5

ansible管理主机

    os: Centos 7, Debian 9, Debian 10

## 角色变量

无

## 初始化项目

- 关闭服务
  - 关闭防火墙
  - 关闭网络服务
  - 关闭selinux
  - 关闭swap
- 系统优化
  - 系统参数调整
  - 修改系统限制
  - 修改系统仓库国内镜像
- 系统设置
  - 修改sshd配置
  - vim环境设置
  - cpu设置为性能模式
- 系统环境设置
  - history格式设置
- 功能启用
  - 安装基础软件
  - 开启systemd journald服务
  - 开启rc.local开机自启动
- 系统升级
  - 升级系统包
  
## 依赖

无

## github地址

https://github.com/lework/Ansible-roles/tree/master/os-init

## Example Playbook
```yaml
- hosts: servers
  roles:
    - os-init
```