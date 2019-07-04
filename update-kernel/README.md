# Ansible Role: update-kernel

升级centos6,7,8内核

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.8.1`
os `Centos 7.4 X64`

## 角色变量
    update_kernel_repo_rpm: ""
    update_kernel_repo_key: "https://www.elrepo.org/RPM-GPG-KEY-elrepo.org"

    update_kernel_reboot: true

## 依赖

没有

## github地址
https://github.com/lework/Ansible-roles/tree/master/update-kernel

## Example Playbook

    - hosts: node1
      roles:
      - update-kernel