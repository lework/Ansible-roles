# Ansible Role: nodejs

安装nodejs

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`
python `2.7.5`
os `Centos 7.4 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    nodejs_version: "6.13.1"

    nodejs_file: "node-v{{ nodejs_version }}-linux-x64.tar.gz"
    nodejs_file_path: "{{ software_files_path }}/{{ nodejs_file }}"
    nodejs_file_url: "http://nodejs.org/dist/v{{ nodejs_version }}/{{ nodejs_file }}"

    npm_config_prefix: "{{ nodejs_install_path }}/nodejs"
    npm_registry: "https://registry.npm.taobao.org"

    nodejs_npm_global_packages: 
     - {'name': 'forever'}


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/nodejs

## Example Playbook

    - hosts: servers
      roles:
        - nodejs
        
    - hosts: server
      roles:
        - { role: nodejs, nodejs_version: "0.12.9", nodejs_npm_global_packages: [{'name':'serve'}]}