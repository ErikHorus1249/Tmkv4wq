from scapy.all import srp,Ether,ARP,conf
import sys
import nmap
import netifaces
import socket
import fcntl
import struct
import re
import netifaces
import ipaddress

# IP + MAC
def Arp(ip,interface):
        result = []
        print("IP range : "+ip + "\t" + "interface : "+interface)
        arp_r = ARP(pdst=ip) # ARP requet 
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r # creat ARP request
        answered, unanswered = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip),timeout=2,iface=interface,inter=0.1)
        for i in answered:
            ip, mac = i[1].psrc, i[1].hwsrc
            print(ip + '\t\t' + mac)
            result.append({'IP':ip,'MAC':mac,'PORTS':portScan(ip)})
        return result

# PORT scanning   
def portScan(ip): 
    result = []# port result of scanning 
    try:# instantiate nmap.PortScanner object
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

# get network interface default
def getDefaultInterface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]

# get ip range
def getIpRange():
    INTER = getDefaultInterface()
    NETMASK = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['netmask'])
    IP = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['addr'])
    return str(ipaddress.ip_network(IP+'/'+NETMASK, strict=False))
    
# get host name
def getHostName(ip):
    return socket.gethostbyaddr('192.168.0.106')[0]

print(Arp(getIpRange(), getDefaultInterface())) # call the method

