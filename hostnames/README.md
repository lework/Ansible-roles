# Ansible Role: hostnames

配置hosts文件的主机名和ip的对应关系。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.5.2`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量
    hostnames_file: "/etc/hosts"
	ipnames: []
	# [{'192.168.77.129': 'master'}, {'192.168.77.130': 'node1'}, {'192.168.77.131': 'node2'}]

## 依赖


## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/hostnames

## Example Playbook
	
    # 添加ip和主机名到/etc/hosts
    - hosts: node1
      roles:
        - hostnames

    # 添加指定的ip和主机名到/etc/hosts
    - hosts: node1 node2 node3
      vars:
        - ipnames:
            '192.168.77.130': 'node1'
            '192.168.77.131': 'node2'
            '192.168.77.132': 'node3'
      roles:
        - hostnames