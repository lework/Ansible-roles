# Ansible Role: tengine

安装tengine

## 介绍
Tengine是由淘宝网发起的Web服务器项目。它在Nginx的基础上，针对大访问量网站的需求，添加了很多高级功能和特性。Tengine的性能和稳定性已经在大型的网站如淘宝网，天猫商城等得到了很好的检验。它的最终目标是打造一个高效、稳定、安全、易用的Web平台。

官方网站：http://tengine.taobao.org/
官方文档地址：http://tengine.taobao.org/documentation.html

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: 2.3.1.0
    os: Centos 7.2 X64
    python: 2.7.5

ansible管理主机

    os: Centos 6.7 X64, Centos 7.2 X64

## 角色变量
   software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    tengine_version: "2.2.0"

    tengine_file: "tengine-{{ tengine_version }}.tar.gz"
    tengine_file_path: "{{ software_files_path }}/{{ tengine_file }}"
    tengine_file_url: "http://tengine.taobao.org/download/tengine-{{ tengine_version }}.tar.gz"

    tengine_temp_path: "/var/tmp/tengine"
    tengine_conf_path: "{{ software_install_path }}/tengine-{{ tengine_version }}/conf/"
    tengine_conf_file_path: "{{ software_install_path }}/tengine-{{ tengine_version }}/conf/nginx.conf"

    tengine_user: 'tengine'
    tengine_group: 'tengine'
    tengine_build_options: ''
    tengine_configure_command: >
      ./configure 
      --prefix={{ software_install_path }}/tengine-{{ tengine_version }}
      --user={{ tengine_user }}
      --group={{ tengine_group }}
      --with-poll_module
      --with-file-aio
      --with-http_sub_module
      --with-http_ssl_module
      --with-http_flv_module
      --with-http_dav_module
      --with-http_mp4_module
      --with-http_stub_status_module
      --with-http_gunzip_module
      --with-http_gzip_static_module
      --with-http_realip_module
      --with-http_slice_module
      --with-http_image_filter_module
      --with-http_auth_request_module
      --with-http_concat_module
      --with-http_random_index_module
      --with-http_secure_link_module
      --with-http_sysguard_module
      --with-http_degradation_module
      --with-http_v2_module
      --http-client-body-temp-path={{ tengine_temp_path }}/client/
      --http-proxy-temp-path={{ tengine_temp_path }}/proxy/
      --http-fastcgi-temp-path={{ tengine_temp_path }}/fcgi/
      --http-uwsgi-temp-path={{ tengine_temp_path }}/uwsgi
      --http-scgi-temp-path={{ tengine_temp_path }}/scgi 
      --with-pcre 
      {{ tengine_build_options }}

    tengine_pidfile: '/var/run/tengine.pid'
    tengine_worker_processes: "{{ ansible_processor_vcpus | default(ansible_processor_count) }}"
    tengine_worker_connections: "10240"
    tengine_multi_accept: "off"
    tengine_pid_file: "/var/run/tengine.pid"

    tengine_logpath: "/var/log/tengine"
    tengine_error_log: "{{ tengine_logpath }}/error.log"
    tengine_access_log: "{{ tengine_logpath }}/access.log"
    tengine_mime_file_path: "mime.types"

    tengine_sendfile: "on"
    tengine_tcp_nopush: "on"
    tengine_tcp_nodelay: "off"

    tengine_keepalive_timeout: "65"
    tengine_keepalive_requests: "1000"

    tengine_client_max_body_size: "64m"

    tengine_server_names_hash_bucket_size: "64"

    tengine_proxy_cache_path: ""

    tengine_extra_conf_options: ""

    tengine_extra_http_options: ""

    tengine_remove_default_vhost: false
    tengine_vhosts: []

    tengine_upstreams: ''

    tengine_proxys: false
    tengine_gzip: false
    tengine_stub_status: false
    tengine_stream: false
    
## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/tengine

## Example Playbook

    默认安装tengine
    - hosts: node1
      roles:
       - tengine

    反向代理
    - hosts: node1
      vars:
       - tengine_vhosts:
            - listen: 80
              locations:
                - name: /
                  proxy_pass: http://192.168.77.135:8080
                  proxy_set_headers:
                    Host: $host
                    X-Real-IP: $remote_addr
                    X-Forwarded-For: $proxy_add_x_forwarded_for
      roles:
       - tengine

    反向代理缓存,采用扩展选项
    - hosts: node1
      vars:
       - tengine_proxy_cache_path: /data/nginx/cache levels=1:2 keys_zone=STATIC:10m inactive=24h max_size=5g
       - tengine_vhosts:
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
       - tengine

    反向负载均衡
    - hosts: node1
      vars:
       - tengine_upstreams:
          - name: upstremtest
            servers:
              - 127.0.0.1:8000 weight=3 max_fails=2 fail_timeout=2
              - 127.0.0.1:8001
              - 127.0.0.1:8002
              - 127.0.0.1:8003 backup
       - tengine_vhosts:
            - listen: 80
              locations:
               - name: /
                 proxy_pass: http://upstremtest
      roles:
       - tengine


## 使用

```
/etc/init.d/tengine 
Usage: /etc/init.d/tengine {start|stop|reload|configtest|status|force-reload|upgrade|restart|reopen_logs}
```