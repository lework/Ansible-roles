# Ansible Role: Jenkins CI

安装Jenkins CI

## 介绍
Jenkins 是一个开源项目，提供了一种易于使用的持续集成系统，使开发者从繁杂的集成中解脱出来，专注于更为重要的业务逻辑实现上。同时 Jenkins 能实施监控集成中存在的错误，提供详细的日志文件和提醒功能，还能用图表的形式形象地展示项目构建的趋势和稳定性。

官方： https://jenkins.io/
github: https://github.com/jenkinsci/jenkins

## 要求

此角色在Debian和RHEL及其衍生产品上运行。

## 测试环境

ansible主机

    ansible: 2.9.1
    os: Centos 7.4 X64
    python: 2.7.5

ansible管理主机

    os: Centos 7, Debian 9, Debian 10

## 角色变量

**默认变量**

```yaml
software_files_path: "/opt/software"

jenkins_version: "2.223"

jenkins_home: /var/lib/jenkins
jenkins_hostname: localhost
jenkins_http_port: 8080
jenkins_jar_location: "{{ jenkins_home }}/jenkins-cli.jar"
jenkins_url_prefix: ""
jenkins_java_options: "-Djenkins.install.runSetupWizard=false"

jenkins_admin_username: admin
jenkins_admin_password: admin

jenkins_updates_url: "https://cdn.jsdelivr.net/gh/lework/jenkins-update-center/updates/tencent/update-center.json"

jenkins_init_changes:
  - option: "JENKINS_ARGS"
    value: "--prefix={{ jenkins_url_prefix }}"
  - option: "{{ jenkins_java_options_env_var }}"
    value: "{{ jenkins_java_options }}"
  
jenkins_plugins_recommended:    
  - ant
  - msbuild
  - gradle
  - maven-plugin
  - nodejs
  - antisamy-markup-formatter
  - build-timeout
  - cloudbees-folder
  - credentials-binding
  - email-ext
  - git
  - git-parameter
  - subversion
  - ldap
  - matrix-auth
  - pam-auth
  - pipeline-stage-view
  - ssh-slaves
  - publish-over-ssh
  - windows-slaves
  - timestamper
  - workflow-aggregator
  - ws-cleanup
  - ansible
  - ansicolor
  - multiple-scms
  - role-strategy
  - show-build-parameters
  
jenkins_plugins_extra: []
```

**Debian 变量**
```yaml
__package:
  - curl
  - gnupg
  - initscripts
  - libselinux1
  - apt-transport-https

__repo_file: jenkins.list
__repo_path: /etc/apt/sources.list.d/


jenkins_file: "jenkins_{{ jenkins_version }}_all.deb"
jenkins_packages_url: "https://mirrors.cloud.tencent.com/jenkins/debian/{{ jenkins_file }}"

jenkins_init_file: /etc/default/jenkins
jenkins_http_port_param: HTTP_PORT
jenkins_java_options_env_var: JAVA_ARGS
```

**RedHat 变量**
```yaml
__package:
  - curl
  - libselinux-python
  - initscripts
  
__repo_file: jenkins.repo
__repo_path: /etc/yum.repos.d/


jenkins_repo_key_url: https://pkg.jenkins.io/redhat/jenkins.io.key

jenkins_file: "jenkins-{{ jenkins_version }}-1.1.noarch.rpm"
jenkins_packages_url: "https://mirrors.cloud.tencent.com/jenkins/redhat/{{ jenkins_file }}"

jenkins_init_file: /etc/sysconfig/jenkins
jenkins_http_port_param: JENKINS_PORT
jenkins_java_options_env_var: JENKINS_JAVA_OPTIONS
```

## 依赖

- java (2.53以上版本需要1.8+)

## github地址

https://github.com/lework/Ansible-roles/tree/master/jenkins

## Example Playbook

```yaml
# 默认安装
- hosts: node1
  roles:
    - { role: java ,java_version: "1.8" }
    - jenkins

# 指定变量
- hosts: node1
  vars:
   - jenkins_version: 2.223
   - jenkins_admin_password: 123456
   - jenkins_http_port： 8888
   - jenkins_plugins_extra：
      - display-console-output
      - ansible
  roles:
   - { role: java ,java_version: "1.8" }
   - jenkins
```

## 使用

```bash
systemctl status jenkins
systemctl start jenkins
systemctl stop jenkins
```
