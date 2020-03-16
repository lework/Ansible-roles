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
UPTIME_INFO=$(printf "%d days, %02dh%02dm%02ds" "$days" "$hours" "$mins" "$secs")

if [ -f /etc/redhat-release ] ; then
#    DIST=$(cat /etc/*-release | grep "DISTRIB_ID" | sed -e 's/DISTRIB_ID=//g' -e 's/"//g')
#    DIST_VER=$(sed -e 's/.*release\ //' -e 's/\ .*//' /etc/redhat-release)
    PRETTY_NAME=$(< /etc/redhat-release)

elif [ -f /etc/debian_version ]; then
   DIST_VER=$(</etc/debian_version)
   PRETTY_NAME="$(grep PRETTY_NAME /etc/os-release | sed -e 's/PRETTY_NAME=//g' -e  's/"//g') ($DIST_VER)"

else
#    DIST=$(cat /etc/*-release | grep "DISTRIB_ID" | sed -e 's/DISTRIB_ID=//g' -e 's/"//g')
#    DIST_VER=$(cat /etc/*-release | grep "VERSION_ID" | sed -e 's/VERSION_ID=//g' -e 's/"//g')
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

# get the load averages
read one five fifteen rest < /proc/loadavg
LOADAVG_INFO="${one}, ${five}, ${fifteen} (1, 5, 15 min)"

# disk
totaldisk=$(df -h -x aufs -x tmpfs --total 2>/dev/null | tail -1)
disktotal=$(awk '{print $2}' <<< "${totaldisk}")
diskused=$(awk '{print $3}' <<< "${totaldisk}")
diskusedper=$(awk '{print $5}' <<< "${totaldisk}")
DISK_INFO="${diskused} / ${disktotal} (${diskusedper})"

# cpu
cpu=$(awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//')
cpun=$(grep -c '^processor' /proc/cpuinfo)
cpuc=$(grep '^cpu cores' /proc/cpuinfo | tail -1 | awk '{print $4}')
cpup=$(grep '^physical id' /proc/cpuinfo | tail -1 | awk '{print $4+1}')
CPU_INFO="${cpu} ${cpup}P ${cpuc}C ${cpun}L"

# mem
#mem_info=$(</proc/meminfo)
#mem_info=$(echo $(echo $(mem_info=${mem_info// /}; echo ${mem_info//kB/})))
#
#for m in $mem_info; do
#  case ${m//:*} in
#    "MemTotal") usedmem=$((usedmem+=${m//*:})); totalmem=${m//*:} ;;
#    "ShMem") usedmem=$((usedmem+=${m//*:})) ;;
#    "MemFree") freemem+=${m//*:} ;;
#    "MemFree"|"Buffers"|"Cached"|"SReclaimable") usedmem=$((usedmem-=${m//*:})) ;;
#  esac
#done
#freemem=$((freemem / 1024))
#usedmem=$((usedmem / 1024))
#totalmem=$((totalmem / 1024))
#mem="${freemem}MiB (Free) ${usedmem}MiB (Usage) / ${totalmem}MiB (Total)"
MEM_INFO="$(cat /proc/meminfo | grep MemFree | awk {'print int($2/1024)'})MB (Free) / $(cat /proc/meminfo | grep MemTotal | awk {'print int($2/1024)'})MB (Total)"

# network
# extranet_ip="and $(curl -s ip.cip.cc)"
IP_INFO="$(ip a | grep glo | awk '{print $2}' | head -1 | cut -f1 -d/) ${extranet_ip:-}"

#clear
echo "$(tput setaf 2)
 ██╗     ███████╗ ██████╗ ██████╗ ███████╗
 ██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██║     █████╗  ██║   ██║██████╔╝███████╗
 ██║     ██╔══╝  ██║   ██║██╔═══╝ ╚════██║
 ███████╗███████╗╚██████╔╝██║     ███████║
 ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═══LEOPS
 
 $(date +"%A, %e %B %Y, %r")
 
 Product............: ${MODEL_INFO}
 OS.................: ${PRETTY_NAME}
 Kernel.............: ${KERNEL}
 CPU................: ${CPU_INFO}
 $(tput setaf 1)
 Hostname...........: $(hostname)
 IP Addresses.......: ${IP_INFO}
 Uptime.............: ${UPTIME_INFO}
 Users online.......: ${USER_NUM}
 Running Processes..: ${RUNNING}
 Memory.............: ${MEM_INFO}
 Load Averages......: ${LOADAVG_INFO}
 Disk Usage.........: ${DISK_INFO} 
 
$(tput sgr0)"
