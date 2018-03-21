# Ansible Role: openresty

安装openresty

## 介绍
OpenResty® 是一个基于 Nginx 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。

官方网站：https://openresty.org/cn/
最佳实践：https://moonbingbing.gitbooks.io/openresty-best-practices/content/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: `2.4.2.0`
    os: `Centos 7.2 X64`
    python: `2.7.5`

ansible管理主机

    os: `Centos 6.7 X64, Centos 7.2 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    openresty_version: "1.13.6.1"

    openresty_file: "openresty-{{ openresty_version }}.tar.gz"
    openresty_file_path: "{{ software_files_path }}/{{ openresty_file }}"
    openresty_file_url: "https://openresty.org/download/openresty-{{ openresty_version }}.tar.gz"

    openresty_conf_path: "{{ software_install_path }}/openresty/nginx/conf/"
    openresty_conf_file_path: "{{ software_install_path }}/openresty/nginx/conf/nginx.conf"

    openresty_user: 'openresty'
    openresty_group: 'openresty'
    openresty_build_options: ''
    openresty_configure_command: >
      ./configure 
      --prefix={{ software_install_path }}/openresty-{{ openresty_version }}
      --user={{ openresty_user }}
      --group={{ openresty_user }}
      --with-http_realip_module
      --with-http_sub_module
      --with-http_auth_request_module
      --with-http_stub_status_module
      --with-stream
      --with-http_gunzip_module
      --with-http_gzip_static_module
      --with-http_iconv_module 
      {{ openresty_build_options }}

    openresty_pidfile: '/var/run/nginx.pid'
    openresty_worker_processes: "{{ ansible_processor_vcpus | default(ansible_processor_count) }}"
    openresty_worker_connections: "1024"
    openresty_multi_accept: "off"

    openresty_logpath: "/var/log/openresty"
    openresty_error_log: "{{ openresty_logpath }}/error.log"
    openresty_access_log: "{{ openresty_logpath }}/access.log"
    openresty_mime_file_path: "mime.types"

    openresty_sendfile: "on"
    openresty_tcp_nopush: "on"
    openresty_tcp_nodelay: "off"

    openresty_keepalive_timeout: "65"
    openresty_keepalive_requests: "100"

    openresty_client_max_body_size: "64m"
    openresty_server_names_hash_bucket_size: "64"
    
    openresty_proxy_cache_path: ""
    openresty_extra_conf_options: ""
    openresty_extra_http_options: ""
    openresty_remove_default_vhost: false
    openresty_vhosts: []
    openresty_upstreams: ''
    openresty_proxys: false
    openresty_gzip: false
    openresty_stub_status: false
    openresty_stream: false


## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/openresty

## Example Playbook

    #默认安装openresty
    - hosts: node1
      roles:
       - openresty
       
    #测试lua脚本
    - hosts: node1
      vars:
      - openresty_vhosts:
        - listen: 80
          locations:
          - name: /
            extra_parameters: |
              content_by_lua '
                  ngx.say("<p>hello, world</p>")
              ';
      roles:
       - openresty

    #反向代理
    - hosts: node1
      vars:
      - openresty_vhosts:
        - listen: 80
          locations:
          - name: /
            proxy_pass: http://192.168.77.135:8080
            proxy_set_headers:
              Host: $host
              X-Real-IP: $remote_addr
              X-Forwarded-For: $proxy_add_x_forwarded_for
      roles:
       - openresty

    #反向代理缓存,采用扩展选项
    - hosts: node1
      vars:
      - openresty_proxy_cache_path: /data/openresty/cache levels=1:2 keys_zone=STATIC:10m inactive=24h max_size=5g
      - openresty_vhosts:
        - listen: 80
          extra_parameters: |
            location / {
                proxy_pass   http://192.168.77.135:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_cache STATIC;
                proxy_cache_valid 200 1d;
                proxy_cache_use_stale error timeout invalid_header updating http_500 http_502 http_503 http_504;
            }
      roles:
       - openresty

    #反向负载均衡
    - hosts: node1
      vars:
      - openresty_upstreams:
        - name: upstremtest
          servers:
          - 127.0.0.1:8000 weight=3 max_fails=2 fail_timeout=2
          - 127.0.0.1:8001
          - 127.0.0.1:8002
          - 127.0.0.1:8003 backup
      - openresty_vhosts:
        - listen: 80
          locations:
          - name: /
            proxy_pass: http://upstremtest
      roles:
       - openresty

    #tcp 端口反向代理
    - hosts: node1
      vars:
      - openresty_stream: true
      - openresty_upstreams:
        - name: upstremtest
          servers:
          - 127.0.0.1:3306 weight=3 max_fails=2 fail_timeout=2
          - 127.0.0.1:3307
      - openresty_vhosts:
        - listen: 23306
          proxy_pass: upstremtest
      roles:
       - openresty
       
       
## 使用

```
/etc/init.d/openresty 
Usage: /etc/init.d/openresty {start|stop|reload|configtest|status|force-reload|upgrade|restart|reopen_logs}

```
