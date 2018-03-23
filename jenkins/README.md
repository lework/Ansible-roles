# Ansible Role: Jenkins CI

安装Jenkins CI

## 介绍
Jenkins 是一个开源项目，提供了一种易于使用的持续集成系统，使开发者从繁杂的集成中解脱出来，专注于更为重要的业务逻辑实现上。同时 Jenkins 能实施监控集成中存在的错误，提供详细的日志文件和提醒功能，还能用图表的形式形象地展示项目构建的趋势和稳定性。

官方： https://jenkins.io/
github: https://github.com/jenkinsci/jenkins

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.2.1.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"

    jenkins_repo_url: https://pkg.jenkins.io/redhat/jenkins.repo
    jenkins_repo_key_url: https://pkg.jenkins.io/redhat/jenkins.io.key
    jenkins_pkg_url: https://pkg.jenkins.io/redhat

    # jenkins_version: 2.46

    jenkins_home: /var/lib/jenkins
    jenkins_hostname: localhost
    jenkins_http_port: 8080
    jenkins_jar_location: "{{ software_files_path }}/jenkins-cli.jar"
    jenkins_url_prefix: ""
    jenkins_java_options: "-Djenkins.install.runSetupWizard=false"

    jenkins_admin_username: admin
    jenkins_admin_password: admin

    jenkins_init_file: /etc/sysconfig/jenkins
    jenkins_init_changes:
      - option: "JENKINS_ARGS"
        value: "--prefix={{ jenkins_url_prefix }}"
      - option: "JENKINS_JAVA_OPTIONS"
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
      - subversion
      - ldap
      - mailer
      - matrix-auth
      - pam-auth
      - pipeline-stage-view
      - ssh-slaves
      - publish-over-ssh
      - windows-slaves
      - timestamper
      - workflow-aggregator
      - ws-cleanup
      
    jenkins_plugins_extra: []


## 依赖
Java (2.53以上版本需要1.8+)

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/jenkins

## Example Playbook
    - hosts: node1
      roles:
        - jenkins
        
    - hosts: node1
      vars：
       - jenkins_version: 2.46
       - jenkins_http_port： 8888
       - jenkins_plugins_extra：
           - display-console-output
           - ansible
      roles:
        - jenkins
        
## 使用
service jenkins
Usage: /etc/init.d/jenkins {start|stop|status|try-restart|restart|force-reload|reload|probe}
