# Ansible Role: deploy-supervisor

以软链接的形式更新应用, 应用由supervisor管理。

## 要求

- 此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`
supervisor `3.3.4`

## 角色变量

```yaml
# 发布的代码文件，包含绝对路径，如:/tmp/test.jar
deploy_file: ""

# 发布的代码文件类型，archive 压缩包 or single 单文件
deploy_file_type: "single"

# supervisor应用的端口
deploy_service_port: "8080"

# 等待多少秒检测端口
deploy_service_port_delay: 1

# 检测端口超时时间
deploy_service_port_timeout: 90

# supervisor应用的名称
deploy_service_name: ""

# 服务文件
deploy_service_file: ""

# 发布服务用户
deploy_service_user: "root"

# 发布服务的家目录
deploy_service_workpath: "/data/web/{{ deploy_service_name }}"

# supervisorctl 管理程序
deploy_service_start_script: "/usr/bin/supervisorctl"

# 验证uri
deploy_verify_uri: ""
deploy_verify_url: "http://127.0.0.1:{{ deploy_service_port }}{{ deploy_verify_uri }}"
deploy_verify_url_status_code: 200
deploy_verify_url_headers:
  Cookie: "ansible deploy check"

# 文件存放的根目录
deploy_file_path: "/data/releases"

# 指定文件前缀,用于存储多个发布文件
deploy_file_prefix: "{{ '%Y%m%d_%H%M' | strftime }}"

# 上线代码的存储目录
deploy_code_online_path: "{{ deploy_file_path }}/{{deploy_file_prefix}}_{{ deploy_file | basename | regex_replace('\\.tgz','') }}"

# 文件保留数量
deploy_file_keep_number: 7

# 是否回滚
deploy_rollback: false
```

## 依赖

- supervisor

## github地址

https://github.com/lework/Ansible-roles/tree/master/deploy-supervisor

## Example Playbook

### 发布代码

```yaml
# 发布单文件
- hosts: node1
  vars:
    - deploy_file: /opt/test.jar
    - deploy_service_name: test_spingboot
    - deploy_service_port: 8084
    - deploy_verify_uri: "/"
  roles:
    - deploy-supervisor
    
    
# 发布压缩包
- hosts: node1
  vars:
    - deploy_file: /opt/test.tgz
    - deploy_file_type: "archive"
    - deploy_service_name: test
    - deploy_service_port: 8084
    - deploy_verify_uri: "/"
  roles:
    - deploy-supervisor
```

# 回滚代码。

> 需指定文件前缀 `deploy_file_prefix`

```yaml
- hosts: node1
  vars:
    - deploy_rollback: true
    - deploy_file: test.jar
    - deploy_service_name: test_spingboot
    - deploy_service_port: 8084
    - deploy_file_prefix: "20200828_0250"
    - deploy_verify_uri: "/"
  roles:
    - deploy-supervisor
```
