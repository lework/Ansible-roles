# Ansible Role: confd

安装confd

confd是一个统一配置管理工具，目前仍在开发中，基于本地文件存储的部署方式已经可以用于生产环境中。

github: https://github.com/kelseyhightower/confd

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    confd_version: "0.15.0"
    confd_file: "confd-{{ confd_version }}-linux-amd64"
    confd_path: "{{ software_install_path }}/confd"
    confd_file_path: "{{ software_files_path }}/{{ confd_file }}"

    confd_file_url: "https://github.com/kelseyhightower/confd/releases/download/v{{ confd_version }}/{{ confd_file }}"

    confd_manager_app: "nginx"
    confd_backend: "etcd"
    confd_backend_node: "http://127.0.0.1:2379"

    confd_interval: 3

    confd_run_opts: >
      -interval {{ confd_interval }}
      -confdir {{ confd_path }}
      -backend {{ confd_backend}}
      -node {{ confd_backend_node}}

## 依赖

etcd nginx

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/confd

## Example Playbook
    
    使用etcd来来配置nginx
    - hosts: node1
      roles:
        - confd
        
## 使用

#### 配置
```
etcdctl set /nginx_app/domain www.myapp.com
etcdctl set /nginx_app/upstream/app0 '10.0.1.100:80'
etcdctl set /nginx_app/upstream/app1 '10.0.1.101:80'
```
#### nginx配置

nginx家目录地址： `/usr/local/nginx`

在`nginx.conf`里增加 `include app.conf`

#### 启动
```
systemctl start confd
```
