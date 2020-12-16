import ipaddress
import socket
import fcntl
import struct
import sys
import subprocess
import netifaces
from scapy.all import srp,Ether,ARP,conf
import time
# net = ipaddress.ip_network('10.13.0.106/255.255.255.0', strict=False)
# print(net)
# ip_addr = socket.gethostbyname(socket.gethostname())
# netmask = ipaddress.IPv4Network('192.168.0.106').netmask
# print(netmask)
# def getDefaultInterface():
#     gws=netifaces.gateways()
#     return gws['default'][netifaces.AF_INET][1]

# def get_netmask(ifname):
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

# print(get_netmask('wlp1s0'))
    
# print(sys.argv)

# ip = '192.168.0.106' #Example
# proc = subprocess.Popen('ifconfig',stdout=subprocess.PIPE)
# while True:
#     line = proc.stdout.readline()
#     if ip.encode() in line:
#         break
# mask = line.rstrip().split(b':')[-1].replace(b' ',b'').decode()
# print(mask)
# print(netifaces.ifaddresses('wlp1s0')[netifaces.AF_INET][0]['netmask'])
# print(netifaces.ifaddresses('wlp1s0'))
# hostname = None
# print(socket.gethostbyaddr('192.168.0.1')[0])
# try:
#     hostname =socket.gethostbyaddr('192.168.0.109')
#     if hostname:
#         print(hostname)
#     else:
#         print('no')
# except socket.herror:
#     print('loi')
def getHost(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def getDefaultInterface():
    gws=netifaces.gateways()
    return gws['default'][netifaces.AF_INET][1]

def getIpRange():
    INTER = getDefaultInterface()
    NETMASK = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['netmask'])
    IP = str(netifaces.ifaddresses(INTER)[netifaces.AF_INET][0]['addr'])
    return str(ipaddress.ip_network(IP+'/'+NETMASK, strict=False))

def scan_ips(interface, ips):
	try:
		print('[*] Start to scan')
		conf.verb = 0 # hide all verbose of scapy
		ether = Ether(dst="ff:ff:ff:ff:ff:ff")
		arp = ARP(pdst = ips)
		answer, unanswered = srp(ether/arp, timeout = 2, iface = interface, inter = 0.1)

		for sent, received in answer:
			print(received.summary())

	except KeyboardInterrupt:
		print('[*] User requested Shutdown')
		print('[*] Quitting...')
		sys.exit(1)

def SCAN_NETWORK(MAC_ADDRESS, IP_RANGE, INTERFACE):
    print("[+] Scanning network ... \n")
    start_time = time.time()
    conf.verb = 0
    if MAC_ADDRESS == "None":
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = IP_RANGE), timeout = 2,   iface=INTERFACE,inter=0.1)
    else:
        ans, unans = srp(Ether(src=MAC_ADDRESS, dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = IP_RANGE), timeout = 2,   iface=INTERFACE,inter=0.1)
    for snd,rcv in ans:
        try:
            hostname = socket.gethostbyaddr(str(rcv[ARP].psrc))[0]
            print(hostname)
            # print(rcv.sprintf(r"%ARP.psrc% ["hostname"] - %Ether.src%"))
        except socket.herror:
            print('loi ko thay host')
    stop_time = time.time()
    total_time = stop_time - start_time 
    print("\n")
    print("[*] Module Completed!")
    print("[*] Scan Duration: %s \n" %(total_time)) 

def Arp(ip,interface):
        count = 0
        result = []
        # time to wait for an answer
        time_out = 3
        print("IP range : "+ip + "\t" + "interface : "+interface)
        arp_r = ARP(pdst=ip) # ARP requet 
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r # creat ARP request
        answered, unanswered = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip),timeout=time_out,iface=interface,inter=0.1)
        for i in answered:
            count += 1
            ip, mac = i[1].psrc, i[1].hwsrc
            host_name = getHost(ip)
            if host_name:
                print(ip + '\t\t' + mac + '\t\t' + host_name)
                result.append({'IP':ip,'MAC':mac,'HOST':host_name})
            else :
                print(ip + '\t\t' + mac)
                result.append({'IP':ip,'MAC':mac})
        print("Devices : "+str(count))
        return result


# host = getHost('192.168.1.71')
# if(host):
#     print(host)

if __name__ == "__main__":
    host_name = socket.getfqdn('192.168.1.16')
    print(host_name)
    # SCAN_NETWORK(None, '192.168.1.6', getDefaultInterface())
    # scan_ips(getDefaultInterface(),getIpRange())
