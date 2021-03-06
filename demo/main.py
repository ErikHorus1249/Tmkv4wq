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
import time 

# IP + MAC
def Arp(ip,interface):
        # hide all verbose of scapy
        # conf.verb = 0 
        count = 0
        result = []
        print('[*] Start to scan')
        # time to wait for an answer
        time_out = 2
        print("IP range : "+ip + "\t" + "interface : "+interface)
        arp_r = ARP(pdst=ip) # ARP requet 
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r # creat ARP request
        answered, unanswered = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip),timeout=time_out,iface=interface,inter=0.1)
        for i in answered:
            count += 1
            ip, mac = i[1].psrc, i[1].hwsrc
            host_name = getHost(ip)
            # port scan ssh or telnet
            if host_name:
                # result.append({'IP':ip,'MAC':mac,'HOST':host_name})
                # result.append({'IP':ip,'MAC':mac,'SSH/TELNET':str(portScan(ip))})
                result.append({'IP':ip,'MAC':mac})
                print(ip + '\t\t' + mac + '\t\t' + host_name)
            else :
                print(ip + '\t\t' + mac + '\t\t\t\t\t' )
                result.append({'IP':ip,'MAC':mac})
        print("Devices : "+str(count))
        return result

def Arp1(interface):
        # hide all verbose of scapy
        # conf.verb = 0 
        count = 0
        result = []
        print('[*] Start to scan')
        # time to wait for an answer
        time_out = 2
        for i in range(0,256):
            ip = '192.168.1.'+str(i)
            print("IP range : "+ip + "\t" + "interface : "+interface)
            arp_r = ARP(pdst=ip) # ARP requet 
            br = Ether(dst='ff:ff:ff:ff:ff:ff')
            request = br/arp_r # creat ARP request
            answered, unanswered = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip),timeout=time_out,iface=interface,inter=0.1)
            for i in answered:
                count += 1
                ip, mac = i[1].psrc, i[1].hwsrc
                host_name = getHost(ip)
                # port scan ssh or telnet
                if host_name:
                    # result.append({'IP':ip,'MAC':mac,'HOST':host_name})
                    # result.append({'IP':ip,'MAC':mac,'SSH/TELNET':str(portScan(ip))})
                    result.append({'IP':ip,'MAC':mac})
                    print(ip + '\t\t' + mac + '\t\t' + host_name)
                else :
                    print(ip + '\t\t' + mac + '\t\t\t\t\t' )
                    result.append({'IP':ip,'MAC':mac})
        print("Devices : "+str(count))
        return result

# PORT ssh or telnet protocol scanning   
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
    # scan host, ports from 22 to 23 (SSH/Telnet)
    nm.scan(ip, '22-23')   
    # get all hosts that were scanned   
    nm.all_hosts()                      
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
def getHost(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

if __name__ == "__main__":
    start_time = time.time()
    ip_range = str(getIpRange())
    # ip_range = '192.168.3.100'
    print(Arp(ip_range, getDefaultInterface()))
    print(Arp(ip_range, getDefaultInterface()))
    # print(Arp1(getDefaultInterface()))
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))

# \b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b
