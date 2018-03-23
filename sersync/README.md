# Ansible Role: sersync

安装sersync

## 介绍
sersync主要用于服务器同步，web镜像等功能。基于boost1.43.0,inotify api,rsync command.开发。由金山公司开发并开源的同步软件。sersync部署在源服务器上，在目标服务器上部署好普通的rsync服务后，在源服务器上启动sersync即可，sersync通过解析xml配置文件来获取相关rsync时的一些策略。

官方地址： https://code.google.com/archive/p/sersync/


## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    sersync_version: "2.5.4"

    sersync_file: "sersync{{ sersync_version }}_64bit_binary_stable_final.tar.gz"
    sersync_file_path: "{{ software_files_path }}/{{ sersync_file }}"
    sersync_file_url: "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/sersync/{{ sersync_file }}"

    sersync_xfs: "false"
    sersync_exclude: [] # ["*.ini","*.txt"]
    sersync_logpath: /var/log/sersync
    sersync_home: "{{ software_install_path }}/sersync"
    sersync_conf: "{{ sersync_home }}/conf"

    sersync_watch: "" # /data/
    sersync_rsync: {} # {"ip":192.168.77.130, "port":873, "name":data1, "user":t1, "pass":123456,"params":"-artuz"}
    sersync_rsync_logfile: "{{ sersync_logpath }}/sersync_rsync_exec.log"
    sersync_rsync_passwordfile: "{{ sersync_conf }}/sersync_rsync.password"
    sersync_rsync_timeout: 100
    sersync_rsync_ssh: "false"
    sersync_failLog: "{{ sersync_logpath }}/rsync_fail_log.sh"

    sersync_inotify_delete: true
    sersync_inotify_createFolder: true
    sersync_inotify_createFile: false
    sersync_inotify_closeWrite: true
    sersync_inotify_moveFrom: true
    sersync_inotify_moveTo: true
    sersync_inotify_attrib: false
    sersync_inotify_modify: false

    sersync_crontab: false
    sersync_schedule: 600

## 依赖

rsync

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/sersync

## Example Playbook

    安装sersync：
    - hosts: node2
      vars:
       - sersync_watch: /data/d1
       - sersync_rsync:
          "ip": 192.168.77.129
          "port": 873
          "name": data1
          "user": t1
          "pass": 123456
          "params": -artuz
      roles:
      - role: sersync

## 使用
/usr/local/sersync/bin/sersync -r -d -o /usr/local/sersync/conf/confxml.xml
