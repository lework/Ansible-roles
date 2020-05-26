#### 服务器环境说明：

ansible版本：2.9.3

系统版本：CentOS Linux release 7.6.1810 

rocketmq版本：4.5.2

| 服务器名称           | IP地址        | 安装角色            |
| -------------------- | ------------- | ------------------- |
| rocketmq-nameserver1 | 192.168.60.94 | nameserver，console |
| rocketmq-nameserver2 | 192.168.60.95 | nameserver          |
| rocketmq-master1     | 192.168.60.96 | master              |
| rocketmq-master2     | 192.168.60.97 | master              |
| rocketmq-slave1      | 192.168.60.98 | slave               |
| rocketmq-slave2      | 192.168.60.99 | slave               |

#### Ansible环境说明：

##### inventory文件路径及内容：

/home/floyd/devops/pv105-ansible/hosts_pve105.conf

（备注：确保ansible_user指定的用户已经添加了无密登录，并且配置了免密sudo）

![image-20200426210700980](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426210700980.png)

roles说明：

/home/floyd/devops/ansible/roles/rocketmq

```python
rocketmq
├── defaults
│   └── main.yml
├── meta
│   └── main.yml
├── tasks
│   ├── configure_broker.yml
│   ├── configure_nameserver.yml
│   ├── configure_os.yml
│   ├── install.yml
│   └── main.yml
└── templates
    ├── mqadmin.j2
    ├── rocketmq_broker.conf.j2
    ├── rocketmq_broker.systemd.j2
    ├── rocketmq_nameserver.conf.j2
    ├── rocketmq_nameserver.systemd.j2
    ├── runbroker.sh.j2
    ├── runserver.sh.j2
    ├── service_broker.sh.j2
    └── service_nameserver.sh.j2
```

/home/floyd/devops/ansible/roles/rocketmq_console

```python
rocketmq_console/
├── defaults
│   └── main.yml
├── meta
│   └── main.yml
├── tasks
│   └── main.yml
└── templates
    ├── rocketmq_console.systemd.j2
    ├── runconsole.sh.j2
    └── service.sh.j2
```



其中defaults目录的main.yml保存的是所有变量的默认值；meta目录存放的当前角色索要依赖的角色配置；tasks目录保存的是各类执行任务的tasks文件；templates目录保存的是配置文件模板以及服务启动脚本模板；

##### playbook说明：

/home/floyd/devops/pv105-ansible/pve105-kafka.yml

（备注：确保software_files_path变量定义的目录已经存在，并且当前登录用户具有目录的读写权限。同时确保目录中中存在对应版本的安装包文件、对应依赖的特定版本的jdk安装包文件。）

![image-20200426220722496](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426220722496.png)

```python
#deploy rocketmq  master slave nameserver
- hosts: rocketmq_test
  gather_facts: yes
  become: true

  vars:
    - software_files_path: '/home/floyd/ansible/software'
    - software_install_path: '/data'
    - rocketmq_user: 'cash'
    - create_user: false
    - rocketmq_brokerClusterName: 'rocketmq-cluster'
#    - rocketmq_flushDiskType: 'SYNC_FLUSH'
    - rocketmq_flushDiskType: 'ASYNC_FLUSH'
    - rocketmq_namesrvAddr: "192.168.60.94:9876;192.168.60.95:9876"
    - rocketmq_autoCreateTopicEnable: true
    - rocketmq_autoCreateSubscriptionGroup: true

  roles:
    - role: rocketmq
      rocketmq_brokerRole: 'SYNC_MASTER'
      rocketmq_listenPort: '10911'
      rocketmq_haListenPort: '10912'
      when: rocketmq_play == 'master'

    - role: rocketmq
      rocketmq_brokerRole: 'SLAVE'
      rocketmq_listenPort: '10921'
      rocketmq_haListenPort: '10922'
      when: rocketmq_play == 'slave'
        
    - role: rocketmq
      rocketmq_nameserver_port: 9876
      when: rocketmq_play == 'nameserver'

#deploy rocketmq  console  nameserver
- hosts: rocketmq_console_test
  gather_facts: yes
  become: true

  vars:
    - software_files_path: '/home/floyd/ansible/software'
    - software_install_path: '/data'
    - rocketmq_console_user: 'cash'
    - createuser: false
    - rocketmq_namesrvAddr: "192.168.60.94:9876;192.168.60.95:9876"
    - rocketmq_console_listen_port: "8080"

  roles:
    - role: rocketmq_console

```



#### 安装部署：

```shell
cd /home/floyd/devops/pv105-ansible/

ansible-playbook -i hosts_pve105.conf pve105-rocketmq.yml
```

执行完成：

![image-20200426221401148](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426221401148.png)



检查安装：

nameserver:

![image-20200426224226708](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426224226708.png)

master:

![image-20200426224309244](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426224309244.png)

console:

![image-20200426224352158](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426224352158.png)



console web界面：

![image-20200426224553255](https://raw.githubusercontent.com/acheng-floyd/markdown_pic/master/img/image-20200426224553255.png)