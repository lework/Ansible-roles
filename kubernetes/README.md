# Ansible Role: kubernetes

以Static Pods方式安装kubernetes 1.10.3 ha 集群。

## 介绍

Kubernetes是一个开源系统，用于自动化容器化应用程序的部署，扩展和管理。

官网: <https://kubernetes.io/>

## 要求

此角色仅在RHEL及其衍生产品上运行。

内存大于4G, 8G最好了。
CPU大于4核, 8核最好了。

## 测试环境

ansible `2.5.2`

python `2.7.5`

os `Centos 7.4 X64`

## 角色变量

    software_install_path: '/usr/local'
    kubernetes_bin_path: '{{ software_install_path }}/kubernetes/bin'
    kubernetes_cni_bin_path: '{{ software_install_path }}/cni/bin'
    kubernetes_cfssl_bin_path: '{{ software_install_path }}/cfssl/bin'
    kubernetes_helm_bin_path: '{{ software_install_path }}/helm/bin'
    kubernetes_calic_bin_path: '{{ software_install_path }}/calic/bin'

    kubernetes_node_packages:
      - socat
      - openssl

    kubernetes_min_ram: 1800

    kubernetes_tmp_path: "/tmp/ansibe.fetch"
    kubernetes_etcd_conf_path: '/etc/etcd'
    kubernetes_etcd_ssl_path: '{{ kubernetes_etcd_conf_path }}/ssl'
    kubernetes_etcd_data_path: "/var/lib/etcd"

    kubernetes_cni_conf_path: "/etc/cni/net.d"
    kubernetes_haproxy_conf_path: "/etc/haproxy"
    kubernetes_images_path: "/opt/software/kubernetes/images"

    kubernetes_log_path: "/var/log/kubernetes"
    kubernetes_conf_path: "/etc/kubernetes"
    kubernetes_addons_conf_path: "{{ kubernetes_conf_path }}/addons"
    kubernetes_pki_path: "{{ kubernetes_conf_path }}/pki"
    kubernetes_manifests_path: "{{ kubernetes_conf_path }}/manifests"
    kubernetes_kubelet_service_path: "/etc/systemd/system/kubelet.service.d"
    kubernetes_kubelet_data_path: "/var/lib/kubelet"

    kubernetes_apiserver_vip: ""
    kubernetes_apiserver_port: "6443"
    kubernetes_cluster_ip: "10.96.0.1"
    kubernetes_cluster_dns: "10.96.0.10"
    kubernetes_cluster_domain: "cluster.local"
    kubernetes_cluster_ip_rang: "10.96.0.0/12"
    kubernetes_cluster_cidr: "10.244.0.0/16"

    kubernetes_dashboard_port: "443"
    kubernetes_haproxy_status_port: "9090"
    kubernetes_haproxy_admin_passwd: "admin123"

    # Kubernetes ingress: nginx,traefik
    kubernetes_ingress_controller: "nginx"

    # Kubernetes master
    kubernetes_apiserver_image: "gcr.io/google_containers/kube-apiserver-amd64:v1.10.3"
    kubernetes_controller_image: "gcr.io/google_containers/kube-controller-manager-amd64:v1.10.3"
    kubernetes_scheduler_image:  "gcr.io/google_containers/kube-scheduler-amd64:v1.10.3"
    kubernetes_etcd_image: "gcr.io/google_containers/etcd-amd64:3.1.13"
    kubernetes_keepalived_image: "lework/keepalived:v1.3.9"
    kubernetes_haproxy_image: "haproxy:1.8.9-alpine"

    # Kube-proxy
    kubernetes_kube_proxy_image: "gcr.io/google_containers/kube-proxy-amd64:v1.10.3"

    # kubernetes dashboard
    kubernetes_dashboard_image: "gcr.io/google_containers/kubernetes-dashboard-amd64:v1.8.3"

    # Kubernetes network
    kubernetes_calico_node_image: "quay.io/calico/node:v3.1.2"
    kubernetes_calico_cni_image: "quay.io/calico/cni:v2.0.5"
    kubernetes_calico_kube_controllers_image: "quay.io/calico/kube-controllers:v2.0.4"

    # Ingress controller
    kubernetes_nginx_ingress_controller_image: "quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.15.0"
    kubernetes_default_http_backend_image: "gcr.io/google_containers/defaultbackend:1.4"
    kubernetes_traefik_ingress_controller_image: "traefik:v1.6.2-alpine"

    # Kube-dns
    kubernetes_kube_dns_image: "gcr.io/google_containers/k8s-dns-kube-dns-amd64:1.14.10"
    kubernetes_kube_dns_dnsmasq_image: "gcr.io/google_containers/k8s-dns-dnsmasq-nanny-amd64:1.14.10"
    kubernetes_kube_dns_sidecar_image: "gcr.io/google_containers/k8s-dns-sidecar-amd64:1.14.10"

    # Kubernetes monitor
    kubernetes_heapster_image: "gcr.io/google_containers/heapster-amd64:v1.5.3"
    kubernetes_heapster_addon_resizer_image: "gcr.io/google_containers/addon-resizer:1.8.1"
    kubernetes_heapster_influxdb_image: "gcr.io/google_containers/heapster-influxdb-amd64:v1.3.3"
    kubernetes_heapster_grafana_image: "gcr.io/google_containers/heapster-grafana-amd64:v4.4.3"

    # Kubernetes logging
    kubernetes_alpine_image: "alpine:3.7"
    kubernetes_elasticsearch_image: "gcr.io/google-containers/elasticsearch:v6.2.4"
    kubernetes_fluentd_image: "gcr.io/google-containers/fluentd-elasticsearch:v2.1.0"
    kubernetes_kibana_image: "docker.elastic.co/kibana/kibana-oss:6.2.4"

    kubernetes_logging: true
    kubernetes_monitor: true

    kubernetes_master: false
    kubernetes_node: false
    kubernetes_addons: false
    kubernetes_ntpd: true
    kubernetes_node_init: true

## 依赖

centos 7.3 以上版本

所需的文件下载链接：`https://pan.baidu.com/s/1BNMJLEVzCE8pvegtT7xjyQ` 密码：`qm4k`

```bash
# yum -y install unzip
# unzip kubernetes-files.zip -d /etc/ansible/roles/kubernetes/files/
```

## github地址

<https://github.com/kuailemy123/Ansible-roles/tree/master/kubernetes>

## Example Playbook

> 请注意, 主机名称请用小写字母, 大写字母会出现找不到主机的问题。

    # /etc/ansibe/hosts
    [k8s-master]
    192.168.77.133
    192.168.77.134
    192.168.77.135
    [k8s-node]
    192.168.77.136
    192.168.77.137
    192.168.77.138
    [k8s-cluster:children]
    k8s-master
    k8s-node
    [k8s-cluster:vars]
    ansible_ssh_pass=123456

    ---
    # 初始化集群, 配置主机名，配置epel源，安装docker
    - hosts: k8s-cluster
      serial: "100%"
      any_errors_fatal: true
      vars:
        - ipnames:
            '192.168.77.133': 'k8s-m1'
            '192.168.77.134': 'k8s-m2'
            '192.168.77.135': 'k8s-m3'
            '192.168.77.136': 'k8s-n1'
            '192.168.77.137': 'k8s-n2'
            '192.168.77.138': 'k8s-n3'
      roles:
        - hostnames
        - repo-epel
        - docker

    # 安装master节点
    - hosts: k8s-master
      any_errors_fatal: true
      vars:
        - kubernetes_master: true
        - kubernetes_apiserver_vip: 192.168.77.140
      roles:
        - kubernetes

    # 安装node节点
    - hosts: k8s-node
      any_errors_fatal: true
      vars:
        - kubernetes_node: true
        - kubernetes_apiserver_vip: 192.168.77.140
      roles:
        - kubernetes
        
    # 安装addons应用
    - hosts: k8s-master
      any_errors_fatal: true
      vars:
        - kubernetes_addons: true
        - kubernetes_ingress_controller: nginx
        - kubernetes_apiserver_vip: 192.168.77.140
      roles:
        - kubernetes

        
## 运行日志

[![asciicast](https://asciinema.org/a/1saMof2HuDhY0ujkoS2UyuSl7.png)](https://asciinema.org/a/1saMof2HuDhY0ujkoS2UyuSl7)

> 安装完集群后, 最好重启集群观察下健壮性。

## 检查集群状态

```bash
kubectl get cs
kubectl get csr
kubectl get nodes
kubectl get all --all-namespaces=true
```

```bash
kubectl -n kube-system logs -f kube-scheduler-k8s-m2
kubectl -n kube-system get po -o wide -l k8s-app=kube-proxy
kubectl -n kube-system get po -l k8s-app=kube-dns
kubectl -n kube-system get po -l k8s-app=calico-node -o wide
calicoctl node status
kubectl -n kube-system get po,svc -l k8s-app=kubernetes-dashboard
kubectl -n kube-system get po,svc | grep -E 'monitoring|heapster|influxdb'
kubectl -n ingress-nginx get pods
kubectl -n kube-system get po -l app=helm
helm version
```

## 查看addons访问信息

> 在第一台master服务器上

```bash
cat ~/k8s_addons_access
```

- dashboard_url: `https://{{kubernetes_apiserver_vip}}:{{ kubernetes_apiserver_port }}/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login`
- grafana_url: `https://{{kubernetes_apiserver_vip}}:{{ kubernetes_apiserver_port }}/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy/`
- elasticsearch_url: `https://{{kubernetes_apiserver_vip}}:{{ kubernetes_apiserver_port }}/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`
- kibana_url: `https://{{kubernetes_apiserver_vip}}:{{ kubernetes_apiserver_port }}/api/v1/namespaces/kube-system/services/kibana-logging/proxy/`