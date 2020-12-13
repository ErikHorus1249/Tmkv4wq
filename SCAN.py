import scapy.all as scapy
import sys
import nmap # import nmap.py module

def Arp(ip):
        result = []
        print(ip)
        arp_r = scapy.ARP(pdst=ip) # ARP requet 
        br = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r
        answered, unanswered = scapy.srp(request, timeout=1)
        # print('\tIP\t\t\t\t\tMAC')
        # print('_' * 37)
        for i in answered:
            ip, mac = i[1].psrc, i[1].hwsrc
            ports = portScan(ip)
            # print(ip, '\t\t' + mac)
            # print('-' * 37)
            result.append({'IP':ip,'MAC':mac,'ports':ports})
        return result
        
def portScan(ip): 
    # result
    result = []

    try:
        nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(0)

    nm.scan(ip, '22-443')      # scan host, ports from 22 to 443
    nm.all_hosts()                      # get all hosts that were scanned
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                result.append(port)
    return result

print(Arp('192.168.0.1/24')) # call the method
