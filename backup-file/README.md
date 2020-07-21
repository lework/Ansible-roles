# Ansible Role: backup-file

备份文件

## 介绍

指定备份目录，在进行压缩后，将文件拉取到本地存放，并发送邮件通知。

## 要求

此角色仅在LINUX上运行。

## 测试环境

- ansible `2.9.10`
- os `Centos 7.7 X64`

## 角色变量
```yaml
# 备份保存目录
backup_file_home: "/opt/backup"

# 项目名称
backup_file_project: "data-test"

backup_file_project_home: "{{ backup_file_home }}/{{ backup_file_project }}"

# 分类
backup_file_classify: "{{ '%Y' | strftime }}"
# year {{ '%Y-%m-%d' | strftime }}
# month {{ '%Y-%m' | strftime }}
# day {{ '%Y-%m-%d' | strftime }}

# 备份文件保存目录, 在ansible管理节点
backup_file_save_path: "{{ backup_file_project_home }}/{{ backup_file_classify }}"

# 保留几个分类，比如保留7个月，1年
backup_file_classify_keep: 7

# 每个分类下，保留每个主机的几个备份文件
backup_file_keep: 7


# [远端]
# 需要备份的目录列表
backup_file_path: []

# 保存备份文件的临时目录
backup_file_tmp_path: "/opt/backup"

# 临时目录保存的文件
backup_file_tmp_keep: 3

# 备份文件的压缩格式
backup_file_format: "gz"
# gz,bz2,tar,xz,zip

# 备份文件的名称
backup_file_name: "{{ backup_file_project }}_{{ ansible_hostname | d(inventory_hostname) }}_{{ '%Y%m%d%H%M%S' | strftime }}.{{ backup_file_format }}"

# [email]
mail_host: ""
mail_port: ""
mail_username: ""
mail_password: ""
mail_to: []
mail_subject: "Backup file Report {{ backup_file_project }} [{{ '%Y-%m-%d' | strftime }}]"

```
## 依赖

根据所设置的压缩格式，需要目标主机上有对应的安装包`tarfile`、`zipfile`、`gzip`和`bzip2`。

## Github地址

https://github.com/lework/Ansible-roles/tree/master/backup-file

## Example Playbook

### 备份es集群配置

```yaml
- hosts: node1 node2 node3
  gather_facts: no
  vars:
    - backup_file_project: es
    - backup_file_path:
      - "/etc/elasticsearch/"
    - mail_host: "smtp.test.com"
    - mail_port: "465"
    - mail_username: "ops@test.com"
    - mail_password: "test"
    - mail_to: ["test@test.com"]
  roles:
    - backup-file
```