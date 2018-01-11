# Ansible Role: grokdebug

安装grokdebug

## 介绍

用于调试logstash中grok表达式。

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`
python `2.6.6`

## 角色变量

	software_files_path: "/opt/software"
	software_install_path: "/usr/local"

	grokdebug_file_url: " https://codeload.github.com/nickethier/grokdebug/zip/master"

	grokdebug_logstash: 4.1.0
	grokdebug_patterns_url: "https://github.com/logstash-plugins/logstash-patterns-core/archive/v{{ grokdebug_logstash }}.tar.gz"

	grokdebug_gem_package:
	 - { name: "cabin", version: "0.5.0"}
	 - { name: "haml", version: "3.1.7"}
	 - { name: "jls-grok", version: "0.10.10"}
	 - { name: "json", version: "1.7.5"}
	 - { name: "kgio", version: "2.8.0"}
	 - { name: "rack", version: "1.4.1"}
	 - { name: "rack-protection", version: "1.2.0"}
	 - { name: "raindrops", version: "0.11.0"}
	 - { name: "shotgun", version: "0.9"}
	 - { name: "tilt", version: "1.3.3"}
	 - { name: "unicorn", version: "4.6.3"}
	 - { name: "sinatra", version: "1.3.3"}
	 
	grokdebug_port: 8080

## 依赖

ruby 2.1.7

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/grokdebug

## Example Playbook

    - hosts: node1
      roles:
        - { role: ruby, ruby_version: 2.1.7, ruby_install_from_source: true}
        - grokdebug
		
## 使用

```
# service grokdebug
Usage:  {start|stop|force-stop|status|restart}
```