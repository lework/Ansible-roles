# Ansible Role: kubernetes-bin

以hyperkube二进制方式安装kubernetes 1.14.3 ha 集群。

## 介绍

Kubernetes是一个开源系统，用于自动化容器化应用程序的部署，扩展和管理。

官网: <https://kubernetes.io/>

## 要求

此角色仅在RHEL及其衍生产品上运行。

内存大于2G, 4G最好了。
CPU大于2核, 4核最好了。

## 测试环境

ansible `2.8.1`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量

	software_install_path: '/usr/local/bin'

	kubernetes_node_packages:
	  - socat
	  - openssl
	  - curl

	kubernetes_ipvsadm_packages:
	  - ipvsadm
	  - ipset
	  - sysstat
	  - conntrack
	  - libseccomp

	kubernetes_min_ram: 1500

	kubernetes_tmp_path: "/tmp/ansibe.fetch"
	kubernetes_etcd_conf_path: '/etc/etcd'
	kubernetes_etcd_ssl_path: '{{ kubernetes_etcd_conf_path }}/ssl'
	kubernetes_etcd_data_path: "/var/lib/etcd"

	kubernetes_haproxy_conf_path: "/etc/haproxy"
	kubernetes_images_path: "/opt/kubernetes/images"

	kubernetes_log_path: "/var/log/kubernetes"
	kubernetes_conf_path: "/etc/kubernetes"
	kubernetes_addons_conf_path: "{{ kubernetes_conf_path }}/addons"
	kubernetes_pki_path: "{{ kubernetes_conf_path }}/pki"
	kubernetes_manifests_path: "{{ kubernetes_conf_path }}/manifests"

	kubernetes_apiserver_vip: "127.0.0.1"
	kubernetes_apiserver_port: "6443"
	kubernetes_cluster_ip: "10.96.0.1"
	kubernetes_cluster_dns: "10.96.0.10"
	kubernetes_cluster_domain: "cluster.local"
	kubernetes_cluster_ip_range: "10.96.0.0/12"
	kubernetes_cluster_cidr: "10.244.0.0/16"

	kubernetes_ingress_ip: ""
	kubernetes_external_dns_ip: ""

	kubernetes_haproxy_status_port: "9090"
	kubernetes_haproxy_admin_passwd: "admin123"


	# kubernetes

	kubernetes_pause_image: "k8s.gcr.io/pause-amd64:3.1"

	# kubernetes dashboard
	kubernetes_dashboard_image: "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1"

	# Kubernetes network
	kubernetes_calico_node_image: "calico/node:v3.7.3"
	kubernetes_calico_cni_image: "calico/cni:v3.7.3"
	kubernetes_calico_ctl_image: "calico/ctl:v3.7.3"
	kubernetes_calico_kube_controllers_image: "calico/kube-controllers:v3.7.3"

	# dns
	kubernetes_coredns_image: "coredns/coredns:1.5.0"
	kubernetes_coredns_etcd_image: "quay.io/coreos/etcd:v3.3.13"
	kubernetes_external_dns_image: "registry.opensource.zalan.do/teapot/external-dns:v0.5.14"

	# Ingress controller
	kubernetes_nginx_ingress_controller_image: "quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.24.1"
	kubernetes_default_http_backend_image: "registry.cn-hangzhou.aliyuncs.com/google_containers/defaultbackend:1.4"

	# Kubernetes monitoring
	kubernetes_metrics_server_image: "k8s.gcr.io/metrics-server-amd64:v0.3.3"
	kubernetes_kube_state_metrics_image: "k8s.gcr.io/kube-state-metrics:v1.6.0"
	kubernetes_addon_resizer_image: "k8s.gcr.io/addon-resizer:1.8.5"
	kubernetes_grafana_image: "grafana/grafana:6.2.4"
	kubernetes_prometheus_node_exporter_image: "prom/node-exporter:v0.18.1"
	kubernetes_prometheus_operator_image: "quay.io/coreos/prometheus-operator:v0.31.0"
	kubernetes_prometheus_configmap_reload_image: "quay.io/coreos/configmap-reload:v0.0.1"
	kubernetes_prometheus_config_reloader_image: "quay.io/coreos/prometheus-config-reloader:v0.31.0"

	# weavescope
	kubernetes_weavescope_image: "docker.io/weaveworks/scope:1.11.2"

	# Kubernetes logging

	kubernetes_master: false
	kubernetes_node: false
	kubernetes_addons: false
	kubernetes_dashboard: true
	kubernetes_metrics_server: true
	kubernetes_external_dns: true
	kubernetes_prometheus: true
	kubernetes_weavescope: true
	kubernetes_helm: true


## 依赖

centos 7.3 以上版本

所需的文件下载链接：`https://pan.baidu.com/s/1eBPPI6kDxvbynH43--ly5g` 密码：`y39z`

将文件解压到role的files目录中
```bash
# yum -y install p7zip
# 7za x k8s-v1.14.3.7za -r -o/opt/
# cp -rf  v1.14.3/* /etc/ansible/roles/kubernetes-bin/files/
```

## github地址

<https://github.com/lework/Ansible-roles/tree/master/kubernetes-bin>

## Example Playbook

> 请注意, 主机名称请用小写字母, 大写字母会出现找不到主机的问题。

    # cat /etc/ansibe/hosts
	[k8s_master]
	192.168.77.130
	192.168.77.131
	192.168.77.132
	[k8s_node]
	192.168.77.133
	192.168.77.134
	[k8s_cluster:children]
	k8s_master
	k8s_node
	[k8s_cluster:vars]
	ansible_ssh_pass=123456

	# cat /etc/ansible/k8s.yml
	---
	# 初始化节点
	- hosts: k8s_cluster
	  serial: "100%"
	  any_errors_fatal: true
	  vars:
		- ipnames:
			'192.168.77.130': 'k8s-m1'
			'192.168.77.131': 'k8s-m2'
			'192.168.77.132': 'k8s-m3'
			'192.168.77.133': 'k8s-n1'
			'192.168.77.134': 'k8s-n2'
	  roles:
		- hostnames
		- { role: ssh-keys, ssh_keys_host: '192.168.77.130' }
		- repo-epel
		- ntp
		- docker
		- update-kernel 

	# 安装master节点
	- hosts: k8s_master
	  any_errors_fatal: true
	  vars:
		- kubernetes_master: true
	  roles:
		- kubernetes-bin

	# 安装node节点
	- hosts: k8s_node
	  any_errors_fatal: true
	  vars:
		- kubernetes_node: true
	  roles:
		- kubernetes-bin

	# 安装addons组件
	- hosts: k8s_master
	  any_errors_fatal: true
	  vars:
		- kubernetes_addons: true
		- kubernetes_ingress_ip: 192.168.77.140
		- kubernetes_external_dns_ip: 192.168.77.141
	  roles:
		- kubernetes-bin

        
## 运行日志

[![asciicast](https://asciinema.org/a/257020.svg)](https://asciinema.org/a/257020)

详细安装说明

[使用ansible来做kubernetes 1.14.3集群高可用的一键部署](https://lework.github.io/2019/07/13/ansible-install-k8s-ha/)

> 安装完集群后, 最好重启集群观察下健壮性。

## 检查集群状态

```bash
kubectl get cs
kubectl get csr
kubectl get nodes
kubectl get ns
kubectl get all --all-namespaces=true
helm version
etcdctl member list
kubectl -n kube-system exec calicoctl -- calicoctl get node -o wide
ipvsadm -Ln
```


## 查看addons访问信息

> 在第一台master服务器上

```bash
cat ~/k8s-addons-access.md

## secret
dashboard_secret: 
eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJlcm5ldGVzLWRhc2hib2FyZC1hZG1pbi10b2tlbi1kZ3p4ayIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrdWJlcm5ldGVzLWRhc2hib2FyZC1hZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImY1NDgwMzQ0LWE0OGYtMTFlOS05MzU3LTAwMGMyOTg4MDFjMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprdWJlcm5ldGVzLWRhc2hib2FyZC1hZG1pbiJ9.wKXs_K633Y-EtfGCPRQjMVsklzpuO7NshhCwgTasmrRpB1MP48kx5pa2D6Mqg6BAv40AGFGdq6m6EK6Beuj-E7brGvvdg3h6P2nDUKBUxEq6dXwBDyNTRiGaI-QmSJHjn8yt59gl7rdgCWrrL_B5bo-umsjV3jKk4tIOMX7RgdqSB6sDkgPoILiC9cNOKl3JIfqH3dXwYHJwJylS2dwvxCbMFpNZtXhCKGP_lciaU0ESr3OGK03-kHCUmWyisX-WnwBbCYvmNIArwhYD8QwHOXU9PI4i2DF48Fg6TAxMFsOpnJd3AvzWCIdaRVmfvQdNTYMEZmkA04oFyPGI_Q9c_g


## host bing
192.168.77.140 kubernetes-dashboard.k8s.local
192.168.77.140 alertmanager.monitoring.k8s.local
192.168.77.140 grafana.monitoring.k8s.local
192.168.77.140 prometheus.monitoring.k8s.local
192.168.77.140 scope.weave.k8s.local


## http access
https://kubernetes-dashboard.k8s.local
http://alertmanager.monitoring.k8s.local
http://grafana.monitoring.k8s.local
http://prometheus.monitoring.k8s.local
http://scope.weave.k8s.local

## DNS
TCP 192.168.77.141
UDP 192.168.77.141

dig @192.168.77.141 A scope.weave.k8s.local +noall +answer
```