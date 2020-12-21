import socket
import scapy.all as scapy
from multiprocessing import Pool
import time
import ipaddress
import netifaces

result = []

def scan_arp1(ip):
    target_ip = ip
    try:
        ans,unans = scapy.arping(target_ip,verbose=0)
        res = ans.summary(lambda s,r: r.sprintf("%Ether.src% %ARP.psrc%") )
        if res != None:
            return res
    except Exception as e:
        print ("Error !".format(e))
        return 

def get_ip(ip_range):
    for ip in ipaddress.IPv4Network(ip_range):
        print(ip)

def run():
    count = 0
    num_procs = 256
    pool = Pool(processes=num_procs)
    for res in pool.imap_unordered(scan_arp1, [str(ip) for ip in ipaddress.IPv4Network('192.168.1.0/24')]):
        if res != None:
            count += 1
            print(res)
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

if __name__ == '__main__':
    start_time = time.time()
    run()
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))