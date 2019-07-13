## secret
dashboard_secret: 
{{ kube_dashboard_secret.stdout }}


## host bing
{% if kubernetes_ingress_ip %}
{{ kubernetes_ingress_ip }} kubernetes-dashboard.k8s.local
{{ kubernetes_ingress_ip }} alertmanager.monitoring.k8s.local
{{ kubernetes_ingress_ip }} grafana.monitoring.k8s.local
{{ kubernetes_ingress_ip }} prometheus.monitoring.k8s.local
{{ kubernetes_ingress_ip }} scope.weave.k8s.local
{% else %}
{{ groups['k8s_node'][0] }} kubernetes-dashboard.k8s.local
{{ groups['k8s_node'][0] }} alertmanager.monitoring.k8s.local
{{ groups['k8s_node'][0] }} grafana.monitoring.k8s.local
{{ groups['k8s_node'][0] }} prometheus.monitoring.k8s.local
{{ groups['k8s_node'][0] }} scope.weave.k8s.local
{% endif %}


## http access
https://kubernetes-dashboard.k8s.local{% if not kubernetes_ingress_ip %}:30443{% endif %}

http://alertmanager.monitoring.k8s.local{% if not kubernetes_ingress_ip %}:30080{% endif %}

http://grafana.monitoring.k8s.local{% if not kubernetes_ingress_ip %}:30080{% endif %}

http://prometheus.monitoring.k8s.local{% if not kubernetes_ingress_ip %}:30080{% endif %}

http://scope.weave.k8s.local{% if not kubernetes_ingress_ip %}:30080{% endif %}


## DNS
{% if kubernetes_external_dns_ip %}
TCP {{ kubernetes_external_dns_ip }}
UDP {{ kubernetes_external_dns_ip }}

```
dig @{{ kubernetes_external_dns_ip }} A scope.weave.k8s.local +noall +answer

```
{% else %}
TCP {{ groups['k8s_master'][0] }} 30053
UDP {{ groups['k8s_master'][0] }} 30053

```
dig @{{ groups['k8s_master'][0] }} -p 30053 A www.baidu.com +noall +answer

```
{% endif %}
