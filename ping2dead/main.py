from pythonping import ping
from multiprocessing import Pool

def ping2dead(ip):
    return [ip,str(ping(ip,verbose=False))]

ips = ['192.168.1.1','192.168.1.8','192.168.1.9','192.168.0.10','192.168.0.17']

def run(ips):
    num_procs = 10 # the number of threads handled
    pool = Pool(processes=num_procs)
    for res in pool.imap_unordered(ping2dead, [ip for ip in ips]):
        if 'Request timed out' in str(res[1]) :
            print('ip'+res[0]+" timeout")
        else :
            print('ip'+res[0]+" Ping successfully")            

def main():
    for each_ip in ips:
        result_ping = ping2dead(each_ip)
        status = str(result_ping[1])
        if 'Request timed out' in status:
            print(result_ping[0]+' oh no timeout')
        else:
            print(result_ping[0]+' ping ok')
    
run(ips)
# main()


