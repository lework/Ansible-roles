# Ansible Role: lua

添加lua语言环境

## 介绍

Lua 是一种轻量小巧的脚本语言，用标准C语言编写并以源代码形式开放， 其设计目的是为了嵌入应用程序中，从而为应用程序提供灵活的扩展和定制功能。
Lua 是巴西里约热内卢天主教大学（Pontifical Catholic University of Rio de Janeiro）里的一个研究小组，由Roberto Ierusalimschy、Waldemar Celes 和 Luiz Henrique de Figueiredo所组成并于1993年开发。

官网: http://www.lua.org/
官方文档: http://www.lua.org/docs.html
wiki: http://lua-users.org/wiki/
编译好的lua：http://luabinaries.sourceforge.net/
lua软件包管理器： https://luarocks.org/
luajit: http://luajit.org/

## 要求

此角色仅在RHEL及其衍生产品上运行。

## 测试环境

ansible `2.3.0.0`
os `Centos 6.7 X64`

## 角色变量
    software_files_path: "/opt/software"
    software_install_path: "/usr/local"

    lua_version: "5.3.4"
    lua_file: "lua-{{ lua_version }}.tar.gz"
    lua_file_path: "{{ software_files_path }}/{{ lua_file }}"
    lua_file_url: " http://www.lua.org/ftp/{{ lua_file }}"

    lua_luarocks_version: "2.4.2"
    lua_luarocks_file: "luarocks-{{ lua_luarocks_version }}.tar.gz"
    lua_luarocks_file_path: "{{ software_files_path }}/{{ lua_luarocks_file }}"
    lua_luarocks_file_url: "http://luarocks.github.io/luarocks/releases/{{ lua_luarocks_file }}"

    lua_luajit_version: "2.0.5"
    lua_luajit_file: "LuaJIT-{{ lua_luajit_version }}.tar.gz"
    lua_luajit_file_path: "{{ software_files_path }}/{{ lua_luajit_file }}"
    lua_luajit_file_url: "http://luajit.org/download/{{ lua_luajit_file }}"

    lua_install_rocks: []
     
    install_luarocks: true
    install_luajit: false

## 依赖

gcc

## github地址
https://github.com/kuailemy123/Ansible-roles/tree/master/lua

## Example Playbook
    # 默认安装lua
    - hosts: node1
      roles:
        - lua
        
    # 安装指定版本的lua
    - hosts: node1
      roles:
        - { role: lua, lua_version: '5.3.3' }
    
    # 安装luajit
    - hosts: node1
      vars:
        - install_luajit: true
      roles:
        - lua