import socket
import scapy.all as scapy
from multiprocessing import Pool
import time
result = []

def scan_arp1(ip):
    target_ip = ip
    # print(target_ip)
    try:
        ans,unans = scapy.arping(target_ip,verbose=0)
        res = ans.summary(lambda s,r: r.sprintf("%Ether.src% %ARP.psrc%") )
        if res != None:
            return res
    except Exception as e:
        print ("Error !".format(e))
        return 

if __name__ == '__main__':
    start_time = time.time()
    num_procs = 256
    tails = range(0,256)
    pool = Pool(processes=num_procs)
    for res in pool.imap_unordered(scan_arp1, [('192.168.1.'+str(tail)) for tail in tails]):
        if res != None:
            print(res)
    print("\n--->  time execution %s s" % round(time.time() - start_time,2))