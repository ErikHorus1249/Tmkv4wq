#! /usr/bin/env python3
from socket import *
import socket
import urllib.request
import json
import netifaces
import ipaddress
import nmap
from scapy.all import *
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# Arp scanning use arp ping(method) in module scapy  
def scan_arp(target_ip):
    try:
        answereds, unanswereds = arping(target_ip, verbose=0)
        return [[answered[1].sprintf("%ARP.psrc%"), answered[1].sprintf("%Ether.src%"), \
                get_info(answered[1].sprintf("%Ether.src%")), \
                scan_port(answered[1].sprintf("%ARP.psrc%"))] \
                for answered in answereds]
    except Exception as e:
        print ("Error !".format(e))
        return []

# MAC vendor lookup
def get_info(mac):
    # url = "http://www.macvendorlookup.com/api/v2/%s" % mac
    url = "http://macvendors.co/api/%s" % mac
    try:
        data = json.load(urllib.request.urlopen(url))
        # print(data['result']['company'])
        return data['result']['company']
    except Exception as e:
        return "Failed to fetch vendor info. Error: {}".format(e)

# Display result
def display_summary(target, results):
    print ("********* Ip range %s *********" % target)
    print ("IP\t\tMAC\t\t\tInfo\t\t\t\t\t\tSSH/Telnet")
    print ('-'*100)
    for result in results:
        print(f'{result[0]:14} {result[1]:20} {result[2]:60} {str(result[3]):10}')
        # print ("%s\t%s\t%s\t\t\t%s" % (result[0], result[1], result[2],result[3]))
        
# Get ip range ex:192.168.0.0/24
def get_IpRange():
    INTER = get_Default_Interface()
    NETMASK = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['netmask'])
    IP = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['addr'])
    return str(ipaddress.ip_network(IP+'/'+NETMASK, strict=False))

# Ssh or telnet protocol port scanning 
def scan_port(ip):
   host = gethostbyname(ip)
   if get_connection(host,22) == 0 or  get_connection(host,23) == 0:
      return True
   return False

def get_connection(host,port):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(1)
      conn = s.connect_ex((host, port))
      return conn

# get network interface default
def get_Default_Interface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]

# main
if __name__ == "__main__":
    start_time = time.time()
    ip = get_IpRange()
    display_summary(ip, scan_arp(ip))
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))

