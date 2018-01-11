# Ansible Role: ruby

安装ruby

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"
    ruby_install_bundler: true
    ruby_install_gems: []
    ruby_install_gems_user: "{{ ansible_user }}"
    ruby_install_from_source: false
    ruby_version: 2.3.0
    ruby_download_url: "http://cache.ruby-lang.org/pub/ruby/ruby-{{ ruby_version }}.tar.gz"
    ruby_file_path: "{{ software_files_path }}/ruby-{{ ruby_version }}.tar.gz"
    ruby_gem_sources: https://gems.ruby-china.org/

## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/ruby

## Example Playbook

    - hosts: servers
      roles:
        - ruby
        
    - hosts: server
      roles:
        - { role: ruby, ruby_install_from_source: true}