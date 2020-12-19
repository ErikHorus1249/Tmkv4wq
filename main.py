#! /usr/bin/env python3

import argparse
import logging
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


def arpscan(target_ip):
    try:
        answereds, unanswereds = arping(target_ip, verbose=0)
        return [[answered[1].sprintf("%ARP.psrc%"), answered[1].sprintf("%Ether.src%"), \
                get_info(answered[1].sprintf("%Ether.src%")), \
                port_Scan(answered[1].sprintf("%ARP.psrc%"))] \
                for answered in answereds]
    except Exception as e:
        print ("Lỗi".format(e))
        return []

def get_info(mac):
    # url = "http://www.macvendorlookup.com/api/v2/%s" % mac
    url = "http://macvendors.co/api/%s" % mac
    try:
        data = json.load(urllib.request.urlopen(url))
        # print(data['result']['company'])
        return data['result']['company']
    except Exception as e:
        return "Failed to fetch vendor info. Error: {}".format(e)

def print_summary(target, results):
    print ("********* arp-scan report for %s *********" % target)
    print ("IP\t\tMAC\t\t\tInfo\t\t\t\t\t\tSSH/Telnet")
    print ('-'*100)
    for result in results:
        print ("%s\t%s\t%s\t\t\t%s" % (result[0], result[1], result[2],result[3]))

def get_IpRange():
    INTER = get_Default_Interface()
    NETMASK = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['netmask'])
    IP = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['addr'])
    return str(ipaddress.ip_network(IP+'/'+NETMASK, strict=False))

# PORT ssh or telnet protocol scanning   
def port_Scan(ip): 
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
def get_Default_Interface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]


if __name__ == "__main__":
    start_time = time.time()
    ip = get_IpRange()
    print_summary(ip, arpscan(ip))
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))

