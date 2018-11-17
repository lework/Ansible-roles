# Ansible Role: Tomcat

安装tomcat应用

## 要求

此角色仅在RHEL及其衍生产品上运行, 支持Centos6\7。

## 测试环境

ansible `2.6.4.0`

os `Centos 7.2 X64`

python `2.7.5`

## 角色变量
    
    software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	java_home: "{{ ansible_env.JAVA_HOME | default('/usr/java/jdk1.7.0_80') }}"

	tomcat_version: "7.0.90"
	tomcat_file: "apache-tomcat-{{ tomcat_version }}.tar.gz"
	tomcat_path: "{{ software_install_path }}/apache-tomcat-{{ tomcat_version }}"
	tomcat_file_path: "{{ software_files_path }}/{{ tomcat_file }}"

	tomcat_file_url: "http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-7/v{{ tomcat_version }}/bin/apache-tomcat-{{ tomcat_version }}.tar.gz"

	tomcat_enabled: true
	tomcat_server_active: false
	tomcat_ajp_active: false
	tomcat_hostname: localhost
	tomcat_user: tomcat
	tomcat_server_port: 8005
	tomcat_catalina_port: 8080
	tomcat_catalina_ajp_port: 8009
	tomcat_catalina_redirect_port: 8443
	tomcat_unpackWARs: true
	tomcat_autoDeploy: true

	tomcat_services_name: "tomcat{% if tomcat_catalina_port != 8080 %}{{ tomcat_catalina_port }}{% endif %}"

	tomcat_work_path: "{{ software_install_path }}/{{ tomcat_services_name }}"
	tomcat_daemon_native_path: "{{ tomcat_work_path }}/bin/commons-daemon-1.1.0-native-src"
	tomcat_native_path: "{{ tomcat_work_path }}/bin/tomcat-native-1.2.17-src"

	tomcat_apr: false
	tomcat_clear_webapps: true

	tomcat_catalina_opts: "-server -Xms1G -Xmx1G -XX:PermSize=256m -XX:MaxPermSize=256m -XX:NewSize=256m -XX:MaxNewSize=256m -Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Djava.awt.headless=true  -Djava.security.egd=file:/dev/./urandom{% if tomcat_apr %} -Djava.library.path=/usr/local/apr/lib {% endif %}-XX:SurvivorRatio=10 -XX:+UseParNewGC -XX:ParallelGCThreads=4 -XX:MaxTenuringThreshold=13 -XX:+UseConcMarkSweepGC -XX:+DisableExplicitGC -XX:+UseCMSInitiatingOccupancyOnly -XX:+ScavengeBeforeFullGC -XX:+UseCMSCompactAtFullCollection -XX:+CMSParallelRemarkEnabled -XX:CMSFullGCsBeforeCompaction=9 -XX:CMSInitiatingOccupancyFraction=60 -XX:+CMSClassUnloadingEnabled -XX:SoftRefLRUPolicyMSPerMB=0 -XX:-ReduceInitialCardMarks -XX:+CMSPermGenSweepingEnabled -XX:CMSInitiatingPermOccupancyFraction=70 -XX:+ExplicitGCInvokesConcurrent -Djava.nio.channels.spi.SelectorProvider=sun.nio.ch.EPollSelectorProvider -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCApplicationConcurrentTime -XX:+PrintHeapAtGC -Xloggc:{{ tomcat_work_path }}/logs/heap_trace.txt -XX:-HeapDumpOnOutOfMemoryError -XX:HeapDumpPath={{ tomcat_work_path }}/logs/HeapDumpOnOutOfMemoryError -Djava.util.Arrays.useLegacyMergeSort=true"

    
## 依赖

java

## github地址

https://github.com/kuailemy123/Ansible-roles/tree/master/tomcat

## Example Playbook
    安装tomcat7
    - hosts: node1
      roles:
       - tomcat

    - hosts: node1
      roles:
       - { role: tomcat, tomcat_catalina_port: 8081, tomcat_server_port: 8005}
       - { role: tomcat, tomcat_catalina_port: 8082, tomcat_server_port: 8006}
    
	安装tomcat7，使用apr
    - hosts: node1
      roles:
       - { role: tomcat, tomcat_apr: true, tomcat_catalina_port: 8007}
	   
    安装tomcat8
    - hosts: node1
      vars:
       - java_version: "1.8"
       - tomcat_version: "8.5.28"
      roles:
       - java
       - tomcat

## 使用

`centos 6`
```
service tomcat
Usage: tomcat ( commands ... )
commands:
  run               Start Tomcat without detaching from console
  start             Start Tomcat
  stop              Stop Tomcat
  version           What version of commons daemon and Tomcat
                    are you running?
```
`centos 7` 
```
systemctl start tomcat
systemctl status tomcat
systemctl stop tomcat
```
