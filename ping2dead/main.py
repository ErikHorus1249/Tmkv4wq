from pythonping import ping
from multiprocessing import Pool
import ipaddress
import time
import subprocess

def ping2dead(ip):
    return [ip,str(ping(ip,verbose=False,timeout=1))]

ips = ['192.168.1.1','192.168.1.8','192.168.1.9','192.168.0.10','192.168.0.17','192.168.0.153', '192.168.0.79', '192.168.0.80', '192.168.0.81', '192.168.0.82', '192.168.0.83', '192.168.0.84', '192.168.0.85', '192.168.0.86', '192.168.0.87', '192.168.0.88', '192.168.0.89', '192.168.0.90', '192.168.0.91', '192.168.0.92', '192.168.0.93', '192.168.0.94', '192.168.0.95', '192.168.0.96', '192.168.0.97', '192.168.0.98']
def get_target():
    ips = []
    for ip in ipaddress.IPv4Network('192.168.0.0/24'):
        ips.append(str(ip))

    return ips
def run(ips):
    num_procs = 1000 # the number of threads handled
    pool = Pool(processes=num_procs)  
    for res in pool.imap_unordered(ping2dead, [str(ip) for ip in ips]):
        if 'Request timed out' in str(res[1]) :
            print('ip'+res[0]+" timeout")
        else :
            print('ip'+res[0]+" Ping successfully")            

def pingNatDead(ip):
    ping_test = subprocess.call('ping %s' % ip)        #Ping host n times
    if ping_test == 0: 
        return  [ip,'ping OK']
    else :
        return [ip,'ping not OK'] 
        

def main():
    start_time = time.time()
    run(get_target())
    print(round(time.time() - start_time,2))
    
def rum(ips):
    for ip in ips:
        print(pingNatDead(ip))

rum(ips)
# main()

