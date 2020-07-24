# Ansible Role: openjdk

添加openjdk环境

## 要求

此角色仅在Linux上运行。

## 测试环境

ansible `2.9.10`
os `Centos 7.7 X64`
python `2.7.5`

## 角色变量

```yaml
software_files_path: "/opt/software"
software_install_path: "/usr/local"

openjdk_setup_binary: false

openjdk_binary_version: "11.0.8_10"
openjdk_binary_file: "OpenJDK{{ openjdk_binary_version.split('.') | first }}U-jdk_x64_linux_{{ openjdk_binary_version }}.tar.gz"
openjdk_binary_file_path: "{{ software_files_path }}/{{ openjdk_binary_file }}"
openjdk_binary_file_url: "https://gh.lework.workers.dev/https://github.com/AdoptOpenJDK/openjdk{{ openjdk_binary_version.split('.') | first }}-upstream-binaries/releases/download/jdk-{{ openjdk_binary_version | regex_replace('_', '+')}}/{{ openjdk_binary_file }}"
openjdk_install_path: "{{ software_install_path }}/"

java_home: "{{ openjdk_install_path }}/openjdk-{{ openjdk_binary_version }}"
```


## 依赖

没有

## github地址

https://github.com/lework/Ansible-roles/tree/master/openjdk

## Example Playbook
    
### 默认安装

> 默认以系统包管理器方式进行安装

```yaml
---

- hosts: node
  roles:
    - openjdk
```

### 使用二进制安装

```yaml
---

- hosts: node
  vars:
    - openjdk_setup_binary: true
  roles:
    - openjdk
```

### 指定二进制版本安装
```yaml
---

- hosts: node
  vars:
    - openjdk_setup_binary: true
    - openjdk_binary_version: 14.0.2
    - openjdk_binary_file: openjdk-14.0.2_linux-x64_bin.tar.gz
    - openjdk_binary_file_url: https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_linux-x64_bin.tar.gz
    - java_home: "/usr/local/jdk-14.0.2"
  roles:
    - openjdk
```