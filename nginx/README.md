# Ansible Role: Nginx

安装Nginx

## 介绍
Nginx ("engine x") 是一个高性能的HTTP和反向代理服务器，也是一个IMAP/POP3/SMTP服务器。Nginx是由Igor Sysoev为俄罗斯访问量第二的Rambler.ru站点开发的，第一个公开版本0.1.0发布于2004年10月4日。其将源代码以类BSD许可证的形式发布，因它的稳定性、丰富的功能集、示例配置文件和低系统资源的消耗而闻名。

官方网站：http://nginx.org/
官方文档地址：http://nginx.org/en/docs/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: `2.3.1.0`
    os: `Centos 7.2 X64`
    python: `2.7.5`

ansible管理主机

    os: `Centos 6.7 X64, Centos 7.2 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    nginx_version: "1.12.1"

    nginx_file: "nginx-{{ nginx_version }}.tar.gz"
    nginx_file_path: "{{ software_files_path }}/{{ nginx_file }}"
    nginx_file_url: "http://nginx.org/download/nginx-{{ nginx_version }}.tar.gz"

    nginx_temp_path: "/var/tmp/nginx"
    nginx_conf_path: "{{ software_install_path }}/nginx-{{ nginx_version }}/conf/"
    nginx_conf_file_path: "{{ software_install_path }}/nginx-{{ nginx_version }}/conf/nginx.conf"

    nginx_user: 'nginx'
    nginx_group: 'nginx'
    nginx_build_options: ''
    nginx_configure_command: >
      ./configure 
      --prefix={{ software_install_path }}/nginx-{{ nginx_version }}
      --user={{ nginx_user }}
      --group={{ nginx_group }}
      --with-stream
      --with-http_ssl_module
      --with-http_flv_module
      --with-http_stub_status_module
      --with-http_gzip_static_module
      --with-http_realip_module
      --http-client-body-temp-path={{ nginx_temp_path }}/client/
      --http-proxy-temp-path={{ nginx_temp_path }}/proxy/
      --http-fastcgi-temp-path={{ nginx_temp_path }}/fcgi/
      --http-uwsgi-temp-path={{ nginx_temp_path }}/uwsgi
      --http-scgi-temp-path={{ nginx_temp_path }}/scgi 
      --with-pcre 
      {{ nginx_build_options }}

    nginx_pidfile: '/var/run/nginx.pid'
    nginx_worker_processes: "{{ ansible_processor_vcpus | default(ansible_processor_count) }}"
    nginx_worker_connections: "1024"
    nginx_multi_accept: "off"
    nginx_pid_file: "/var/run/nginx.pid"

    nginx_logpath: "/var/log/nginx"
    nginx_error_log: "{{ nginx_logpath }}/error.log"
    nginx_access_log: "{{ nginx_logpath }}/access.log"
    nginx_mime_file_path: "mime.types"

    nginx_sendfile: "on"
    nginx_tcp_nopush: "on"
    nginx_tcp_nodelay: "off"

    nginx_keepalive_timeout: "65"
    nginx_keepalive_requests: "100"

    nginx_client_max_body_size: "64m"
    nginx_server_names_hash_bucket_size: "64"

    nginx_proxy_cache_path: ""
    nginx_extra_conf_options: ""
    nginx_extra_http_options: ""

    nginx_remove_default_vhost: false
    nginx_vhosts: []
    
    nginx_upstreams: ''
    nginx_proxys: false
    nginx_gzip: false
    nginx_stub_status: false
    nginx_stream: false
    
## 依赖

没有

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/nginx

## Example Playbook
    默认安装nginx

    - hosts: node1
      roles:
       - nginx

    反向代理
    - hosts: node1
      vars:
       - nginx_vhosts:
            - listen: 80
              locations:
                - name: /
                  proxy_pass: http://192.168.77.135:8080
                  proxy_set_headers:
                    Host: $host
                    X-Real-IP: $remote_addr
                    X-Forwarded-For: $proxy_add_x_forwarded_for
      roles:
       - { role: nginx }

    反向代理缓存,采用扩展选项
    - hosts: node1
      vars:
       - nginx_proxy_cache_path: /data/nginx/cache levels=1:2 keys_zone=STATIC:10m inactive=24h max_size=5g
       - nginx_vhosts:
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
       - { role: nginx }

    反向负载均衡
    - hosts: node1
      vars:
       - nginx_upstreams:
          - name: upstremtest
            servers:
              - 127.0.0.1:8000 weight=3 max_fails=2 fail_timeout=2
              - 127.0.0.1:8001
              - 127.0.0.1:8002
              - 127.0.0.1:8003 backup
       - nginx_vhosts:
            - listen: 80
              locations:
               - name: /
                 proxy_pass: http://upstremtest
      roles:
       - { role: nginx }

    tcp 端口反向代理
    - hosts: node1
      vars:
       - nginx_stream: true
       - nginx_upstreams:
          - name: upstremtest
            servers:
              - 127.0.0.1:3306 weight=3 max_fails=2 fail_timeout=2
              - 127.0.0.1:3307
       - nginx_vhosts:
            - listen: 3306
              proxy_pass: upstremtest
      roles:
       - { role: nginx }


## 使用

```
/etc/init.d/nginx 
Usage: /etc/init.d/nginx {start|stop|reload|configtest|status|force-reload|upgrade|restart|reopen_logs}
```