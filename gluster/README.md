# Ansible Role: gluster

安装gluster 分布式存储集群

## 介绍
Gluster是一款免费的开源软件可扩展网络文件系统。

官方网站：https://www.gluster.org/
官方文档地址：https://docs.gluster.org/en/latest/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.2`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    gluster_version: "4.1"

    gluster_packages: 
      - xfsprogs

    gluster_volume_name: "gluster_data"
    gluster_volume_replica: "{{ ansible_play_hosts.__len__() }}"

    gluster_volume_brick: "/gluster_brick"

    gluster_volume_create: >
      gluster volume create {{ gluster_volume_name}}
      replica {{ gluster_volume_replica }}
      {% for h in play_hosts %}{{ hostvars[h].ansible_hostname }}:{{ gluster_volume_brick }} {% endfor %}

    gluster_volume_start: >
     gluster volume start {{ gluster_volume_name}}

    gluster_hostnames: true
    gluster_epel: true
    gluster_init: true
    gluster_client: false
    gluster_client_mount_src: ''
    gluster_client_mount_dest: ''

## 依赖

hostnames
repo-epel

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/gluster

## Example Playbook

    安装集群
    - hosts: node1 node2 node3
      vars:
        - ipnames:
            '192.168.77.133': 'data-node1'
            '192.168.77.134': 'data-node2'
            '192.168.77.135': 'data-node3'
      roles:
       -  gluster
       
    安装集群, 自定义副本
    - hosts: node1 node2 node3
      vars:
        - ipnames:
            '192.168.77.133': 'data-node1'
            '192.168.77.134': 'data-node2'
            '192.168.77.135': 'data-node3'
        - gluster_volume_brick: '/export/sdb1/brick'
        - gluster_volume_create: >
            gluster volume create replvol repl 2 data-node1:/export/sdb1/brick data-node2:/export/sdb1/brick
        - gluster_volume_start: >
            gluster volume start replvol
      roles:
       -  gluster
       
    客户端挂载
    - hosts: node4
      vars:
        - ipnames:
            '192.168.77.133': 'data-node1'
            '192.168.77.134': 'data-node2'
            '192.168.77.135': 'data-node3'
        - gluster_client: true
        - gluster_client_mount_src: 'data-node1:/gluster_data'
        - gluster_client_mount_dest: '/mnt'
      roles:
       -  gluster
    
       
## 使用
```
yum -y install glusterfs-fuse
mount -t glusterfs data-node1:/gluster_data /mnt
```

