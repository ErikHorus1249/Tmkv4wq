import ipaddress
import socket
import fcntl
import struct
import sys
import subprocess
import netifaces
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
print(netifaces.ifaddresses('wlp1s0')[netifaces.AF_INET][0]['netmask'])
print(netifaces.ifaddresses('wlp1s0')[netifaces.AF_INET][0]['addr'])