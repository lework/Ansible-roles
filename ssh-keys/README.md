# Ansible Role: ssh keys

在主机之间实现免密码登录。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`
os `Centos 6.7 X64`
python `2.7.5`

## 角色变量
    ssh_keys_host  设置指定主机的ip地址

## 依赖

ssh

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/ssh-keys

## Example Playbook
    实现各主机之间免密码登录
    - hosts: node1 node2 node3
      roles:
       - ssh-keys
    
    实现指定主机(ssh_keys_host)免密码登录其他主机
    - hosts: node1 node2 node3
      roles:
       - { role: ssh-keys, ssh_keys_host: '192.168.77.129' }
