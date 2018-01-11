# Ansible Role: EPEL Repository

EPEL使用*[中国科学技术大学](http://mirrors.ustc.edu.cn/)* 作为yum源，并工作在RHEL/CentOS操作系统上。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量

角色默认变量都放在 `defaults/main.yml`文件中:

    epel_source_url: "http://mirrors.ustc.edu.cn"
    epel_repo_url: "{{ epel_source_url }}/epel/epel-release-latest-{{ ansible_distribution_major_version }}.noarch.rpm"
    epel_repo_gpg_key_url: "/etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-{{ ansible_distribution_major_version }}"
    epel_repofile_path: "/etc/yum.repos.d/epel.repo"
    epel_testing_repofile_path: "/etc/yum.repos.d/epel-testing.repo"
    change_epel: 'True'


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/repo-epel

## Example Playbook

    - hosts: servers
      roles:
        - repo-epel
    - host： servers
      roles:
        - {role: repo-epel, epel_source_url: "https://mirrors.tuna.tsinghua.edu.cn" }