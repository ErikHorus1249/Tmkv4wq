from scapy.all import srp,Ether,ARP,conf
import sys
import nmap
import netifaces
import socket
import fcntl
import struct
import re

# IP + MAC
def Arp(ip,interface):
        result = []
        print("IP range : "+ip + "\t" + "interface : "+interface)
        arp_r = ARP(pdst=ip) # ARP requet 
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r # creat ARP request
        answered, unanswered=srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip),timeout=1,iface=interface,inter=0.1)
        for i in answered:
            ip, mac = i[1].psrc, i[1].hwsrc
#            ports = portScan(ip) #get port
            # display
            print('\033[36m' + ip + '\t\t' + mac)
            # print('-' * 37)
            result.append({'IP':ip,'MAC':mac})
        return result


# PORTS        
def portScan(ip): 
    # port result of scanning 
    result = []
    # instantiate nmap.PortScanner object
    try:
        nm = nmap.PortScanner()         
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(0)

    nm.scan(ip, '22-443')      # scan host, ports from 22 to 443 (limit)
    nm.all_hosts()                      # get all hosts that were scanned
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                result.append(port)
    return result

def getDefaultInterface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]

def getLocalIPv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    return ip

def getIpRange(ip):
    tail = ".0/24"
    match = re.search(r'192.168.[0123456789]+', ip)
    if match: #nếu tồn tại chuỗi khớp                     
        return match.group()+tail
    else:
        print ('no match!')


print(Arp(getIpRange(getLocalIPv4()), getDefaultInterface())) # call the method

