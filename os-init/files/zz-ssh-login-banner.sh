#!/bin/sh
#
# @Time    : 2020-02-04
# @Author  : lework
# @Desc    : ssh login banner

# os
upSeconds="$(cut -d. -f1 /proc/uptime)"
secs=$((${upSeconds}%60))
mins=$((${upSeconds}/60%60))
hours=$((${upSeconds}/3600%24))
days=$((${upSeconds}/86400))
UPTIME_INFO=$(printf "%d days, %02dh %02dm %02ds" "$days" "$hours" "$mins" "$secs")

if [ -f /etc/redhat-release ] ; then
    PRETTY_NAME=$(< /etc/redhat-release)

elif [ -f /etc/debian_version ]; then
   DIST_VER=$(</etc/debian_version)
   PRETTY_NAME="$(grep PRETTY_NAME /etc/os-release | sed -e 's/PRETTY_NAME=//g' -e  's/"//g') ($DIST_VER)"

else
    PRETTY_NAME=$(cat /etc/*-release | grep "PRETTY_NAME" | sed -e 's/PRETTY_NAME=//g' -e 's/"//g')
fi

if [[ -d "/system/app/" && -d "/system/priv-app" ]]; then
    model="$(getprop ro.product.brand) $(getprop ro.product.model)"

elif [[ -f /sys/devices/virtual/dmi/id/product_name ||
        -f /sys/devices/virtual/dmi/id/product_version ]]; then
    model="$(< /sys/devices/virtual/dmi/id/product_name)"
    model+=" $(< /sys/devices/virtual/dmi/id/product_version)"

elif [[ -f /sys/firmware/devicetree/base/model ]]; then
    model="$(< /sys/firmware/devicetree/base/model)"

elif [[ -f /tmp/sysinfo/model ]]; then
    model="$(< /tmp/sysinfo/model)"
fi

MODEL_INFO=${model}
KERNEL=$(uname -srmo)
USER_NUM=$(who -u | wc -l)
RUNNING=$(ps ax | wc -l | tr -d " ")

# disk
totaldisk=$(df -h -x aufs -x tmpfs -x overlay --total 2>/dev/null | tail -1)
disktotal=$(awk '{print $2}' <<< "${totaldisk}")
diskused=$(awk '{print $3}' <<< "${totaldisk}")
diskusedper=$(awk '{print $5}' <<< "${totaldisk}")
DISK_INFO="\033[0;33m${diskused}\033[0m of \033[0;34m${disktotal}\033[0m disk space used (\033[0;33m${diskusedper}\033[0m)"

# cpu
cpu=$(awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//')
cpun=$(grep -c '^processor' /proc/cpuinfo)
cpuc=$(grep '^cpu cores' /proc/cpuinfo | tail -1 | awk '{print $4}')
cpup=$(grep '^physical id' /proc/cpuinfo | wc -l)
CPU_INFO="${cpu} ${cpup}P ${cpuc}C ${cpun}L"

# get the load averages
read one five fifteen rest < /proc/loadavg
LOADAVG_INFO="\033[0;33m${one}\033[0m / ${five} / ${fifteen} with \033[0;34m$(( cpun*cpuc ))\033[0m core(s) at \033[0;34m$(grep '^cpu MHz' /proc/cpuinfo | tail -1 | awk '{print $4}')\033 MHz"

# mem
MEM_INFO="$(cat /proc/meminfo | awk '/MemTotal:/{total=$2/1024/1024;next} /MemAvailable:/{use=total-$2/1024/1024; printf("\033[0;33m%.2fGiB\033[0m of \033[0;34m%.2fGiB\033[0m RAM used (\033[0;33m%.2f%\033[0m)",use,total,(use/total)*100);}')"

# network
# extranet_ip=" and $(curl -s ip.cip.cc)"
IP_INFO="$(ip a | grep glo | awk '{print $2}' | head -1 | cut -f1 -d/)${extranet_ip:-}"

# info
echo -e "\033[0;32m
 ██╗     ███████╗ ██████╗ ██████╗ ███████╗
 ██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║     █████╗  ██║   ██║██████╔╝███████╗
 ██║     ██╔══╝  ██║   ██║██╔═══╝ ╚════██║
 ███████╗███████╗╚██████╔╝██║     ███████║
 ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═══ LEOPS
 \033[0m

 Information as of: \033[1;34m$(date +"%Y-%m-%d %T")\033[0m
 
 \033[0;1;31mProduct\033[0m............: ${MODEL_INFO}
 \033[0;1;31mOS\033[0m.................: ${PRETTY_NAME}
 \033[0;1;31mKernel\033[0m.............: ${KERNEL}
 \033[0;1;31mCPU\033[0m................: ${CPU_INFO}

 \033[0;1;31mHostname\033[0m...........: \033[0;34m$(hostname)\033[0m
 \033[0;1;31mIP Addresses\033[0m.......: \033[1;34m${IP_INFO}\033[0m
 
 \033[0;1;31mUptime\033[0m.............: \033[0;33m${UPTIME_INFO}\033[0m
 \033[0;1;31mMemory\033[0m.............: ${MEM_INFO}
 \033[0;1;31mLoad Averages\033[0m......: ${LOADAVG_INFO}
 \033[0;1;31mDisk Usage\033[0m.........: ${DISK_INFO} 

 \033[0;1;31mUsers online\033[0m.......: \033[0;34m${USER_NUM}\033[0m
 \033[0;1;31mRunning Processes\033[0m..: \033[0;34m${RUNNING}\033[0m
"