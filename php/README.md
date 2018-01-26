# Ansible Role: php

安装php7环境, 使用php-fpm管理。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.4.2.0`
os `Centos 7.2 X64`
python `2.7.5`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    php_version: "7.2.1"

    php_file: "php-{{ php_version }}.tar.gz"
    php_file_path: "{{ software_files_path }}/{{ php_file }}"
    php_install_path: "{{ software_install_path }}/php-{{ php_version }}"
    php_file_url: "http://cn2.php.net/distributions/{{ php_file }}"

    php_rpm_url: "https://mirror.webtatic.com/yum/el7/webtatic-release.rpm"

    php_install_from_source: false

    php_user: "apache"
    php_group: "apache"

    php_conf_paths: "/etc"
    php_extension_conf_paths: "/etc/php.d"
    php_fpm_conf_path: "/etc/fpm"
    php_fpm_pool_conf_path: "/etc/php-fpm.d"

    php_apcu_file_url: "https://github.com/krakjoe/apcu/archive/v5.1.9.tar.gz"
    php_apcu_file: "apcu-5.1.9.tar.gz"
    php_apcu_file_path: "{{ software_files_path }}/{{ php_apcu_file }}"
    php_apcu_configure_command: >
        ./configure
        --enable-apcu
        --enable-apcu-mmap
        --with-php-config={{ php_install_path }}/bin/php-config
     
    php_source_configure_command: >
        ./configure
        --prefix={{ php_install_path }}
        --exec-prefix={{ php_install_path }}
        --bindir={{ php_install_path }}/bin
        --sbindir={{ php_install_path }}/sbin
        --includedir={{ php_install_path }}/include
        --libdir={{ php_install_path }}/lib/php
        --mandir={{ php_install_path }}/php/man
        --with-config-file-path={{ php_conf_paths }}
        --with-config-file-scan-dir={{ php_extension_conf_paths }}
        --with-mcrypt=/usr/include
        --with-mhash
        --with-openssl
        --with-mysqli=shared,mysqlnd
        --with-pdo-mysql=shared,mysqlnd
        --with-gd
        --with-curl
        --with-iconv
        --with-gmp
        --with-pspell
        --with-zlib
        --with-xmlrpc
        --with-gettext
        --with-curl
        --with-jpeg-dir
        --with-freetype-dir
        --enable-zip
        --enable-wddx
        --enable-inline-optimization=
        --enable-shared
        --enable-xml
        --enable-bcmath
        --enable-shmop
        --enable-sysvmsg
        --enable-sysvsem
        --enable-sysvshm
        --enable-mbregex
        --enable-mbstring
        --enable-ftp
        --enable-gd-native-ttf
        --enable-gd-jis-conv
        --enable-pcntl
        --enable-pdo
        --enable-sockets
        --enable-soap
        --enable-session
        --enable-opcache
        --enable-fpm
        --disable-debug
        --disable-rpath
        --disable-fileinfo
        --without-gdbm
        --without-pear
        
        
    php_enable_php_fpm: true
    php_fpm_listen: "127.0.0.1:9000"
    php_fpm_listen_allowed_clients: "127.0.0.1"
    php_fpm_pm_max_children: 50
    php_fpm_pm_start_servers: 5
    php_fpm_pm_min_spare_servers: 5
    php_fpm_pm_max_spare_servers: 5

    # OpCache settings.
    php_opcache_zend_extension: "opcache.so"
    php_opcache_enable: "1"
    php_opcache_enable_cli: "0"
    php_opcache_memory_consumption: "96"
    php_opcache_interned_strings_buffer: "16"
    php_opcache_max_accelerated_files: "4096"
    php_opcache_max_wasted_percentage: "5"
    php_opcache_validate_timestamps: "1"
    php_opcache_revalidate_path: "0"
    php_opcache_revalidate_freq: "2"
    php_opcache_max_file_size: "0"
    php_opcache_blacklist_filename: ""

    # APCu settings.
    php_enable_apcu: true
    php_apc_shm_size: "96M"
    php_apc_enable_cli: "0"

    php_expose_php: "On"
    php_memory_limit: "256M"
    php_max_execution_time: "60"
    php_max_input_time: "60"
    php_max_input_vars: "1000"
    php_input_nesting_level: "64"
    php_realpath_cache_size: "32K"

    php_file_uploads: "On"
    php_upload_max_filesize: "64M"
    php_max_file_uploads: "20"

    php_post_max_size: "32M"
    php_date_timezone: "Asia/Shanghai"
    php_allow_url_fopen: "On"

    php_sendmail_path: "/usr/sbin/sendmail -t -i"
    php_output_buffering: "4096"
    php_short_open_tag: "Off"
    php_disable_functions: []

    php_session_cookie_lifetime: 0
    php_session_gc_probability: 1
    php_session_gc_divisor: 1000
    php_session_gc_maxlifetime: 1440
    php_session_save_handler: files
    php_session_save_path: "/tmp"

    php_error_reporting: "E_ALL & ~E_DEPRECATED & ~E_STRICT"
    php_display_errors: "Off"
    php_display_startup_errors: "Off"


## 依赖

epel

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/php

## Example Playbook
    
    rpm方式安装
    - hosts: node1
      roles:
        - php
        
    源码方式安装
    - hosts: node1
      roles:
        - { role: php, php_install_from_source: true }

## 使用

```
systemctl start php-fpm
systemctl stop php-fpm
```