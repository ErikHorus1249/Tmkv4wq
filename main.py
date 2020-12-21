import socket
import scapy.all as scapy
from multiprocessing import Pool
import time
import ipaddress
import netifaces
import json
from socket import *
import socket
import urllib.request
# from scapy.all import *
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

result = []

# Arp scanning use arp ping(method) in module scapy
def scan_arp(ip):
    target_ip = ip
    ssh_port,telnet_port = 22, 23 
    try:
        ans,unans = scapy.arping(target_ip,verbose=0)
        for an in ans:
            return [an[1].sprintf("%ARP.psrc%"), an[1].sprintf("%Ether.src%"), \
                get_info(an[1].sprintf("%Ether.src%")), \
                scan_port(an[1].sprintf("%ARP.psrc%"), ssh_port), \
                scan_port(an[1].sprintf("%ARP.psrc%"), telnet_port)] \

    except Exception as e:
        print ("Error !".format(e))
        print(e)
        return 

# MAC vendor lookup
def get_info(mac):
    url = "http://macvendors.co/api/%s" % mac
    try:
        data = json.load(urllib.request.urlopen(url))
        return data['result']['company']
    except Exception as e:
        return 'Unknown'

# Ssh or telnet protocol port scanning 
def scan_port(ip, port):
   host = gethostbyname(ip)
   if get_connection(host,port) == 0 or get_connection(host,port) == 0:
      return True
   return False
# Enable port checking 
def get_connection(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(1)
      conn = s.connect_ex((host, port))
      return conn

# Get ip range ex:192.168.0.0/24
def get_ip(ip_range):
    for ip in ipaddress.IPv4Network(ip_range):
        print(ip)

def run():
    num_procs = 256 # the number of threads handled
    pool = Pool(processes=num_procs)
    ip_range = get_IpRange() 
    print(ip_range)
    print ('-'*110)
    print ("IP\t\tMAC\t\t\tInfo\t\t\t\t\t\t\tSSH\tTelnet")
    print ('-'*110)
    for res in pool.imap_unordered(scan_arp, [str(ip) for ip in ipaddress.IPv4Network(ip_range)]):
        if res != None:
            print(f'{res[0]:14} {res[1]:20} {res[2]:59} {str(res[3]):8} {str(res[4]):5}')

# Get ip range ex:192.168.0.0/24
def get_IpRange():
    INTER = get_Default_Interface()
    NETMASK = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['netmask'])
    IP = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['addr'])
    return str(ipaddress.ip_network(IP+'/'+NETMASK, strict=False))

# get network interface default
def get_Default_Interface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]

# Main
if __name__ == '__main__':
    start_time = time.time()
    run()
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))